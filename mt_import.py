#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Skript/knihovna pro import data z automatu Mitutoyo do DB
#
# (C) Miloslav Semler
#

import os
import sys
import re
import codecs
from datetime import datetime
from decimal import Decimal
from lib.luminofory import Tabulky

# prochazeni adresaru/vyhledavani souboru

def parse_data(tabulky, filename):
	print "zpracovavam soubor", filename,
	f = codecs.open(filename, mode = "rb", encoding="cp1250")
	mereni = {}
	part = None
	for line in f:
		m = re.match(u"^Datum/Čas\:([0-9]+/[0-9]+/[0-9]+)\s+([0-9]+\:[0-9]+\:[0-9]+)\s*$", line, re.I|re.U)
		if m <> None:
			mereni['cas'] = datetime.strptime(m.group(1)+' '+m.group(2), "%d/%m/%y %H:%M:%S")
			continue
		m = re.match(u"^Drawing No / Title\: ([0-9A-Z\-]+) /([\w,\.\s]+)- part ([0-9]+) \\(ČP\\)\s*$", line, re.I|re.U)
		if m <> None:
			part = m.group(3)
			continue
		m = re.match(u"^Order No\:(PV)/([0-9]{4})/([0-9]+)\s*$", line, re.I|re.U)
		if m <> None:
			mereni['pruvodka'] = (int(m.group(2)) - 1900)*10000000 + int(m.group(3))
			continue
		# blok dat zpracovava druhy for cyklus
		m = re.match("^[_]{36,}\s*$", line, re.I|re.U)
		if m <> None:
			break
	# zkontrolovat, jestli tam uz mereni nahodou neni
	if tabulky.mt_mereni.get(params=['count(*) as cnt'], search = mereni)[0]['cnt'] > 0:
		f.close()
		print " preskakuji"
		return

	# nastavit cast mereni
	mereni['cast_mereni'] = part 
	# kod plata ....
	m = re.match("([A-Za-z0-9]+)_[12]\.out", os.path.basename(filename), re.I|re.U)
	if m <> None:
		mereni['kod'] = m.group(1)
	
	# jinak pokracujeme dale...	
	idcko = tabulky.mt_mereni.insert(mereni)

	# vybrat klice pro rozmerovou kontrolu
	data = tabulky.tolerance_nazvy.get(params=['id', 'mt_conf'], search={'mt_conf':{'not': None}, 'rozm': True})
	# naskladat do pole
	pole2id = {}
	for item in data:
		# print item
		if item['mt_conf'].has_key(str(part)):
			k = item['mt_conf'][part]
			# muze se stat, ze jeden rozmer je na vice radkach, pak se uklada a prumeruje
			if type(k) == type([]):
				for key in k:
					pole2id[key] = item['id']
			else:
				pole2id[k] = item['id']
	# print pole2id

	# zpracovani dat
	poradi_delka = 1
	poradi_uhel = 1
	pozice = 1
	# pole udaju ke kusu
	# inserty nutno provadet az po pripadnem prumerovani
	mt_hodnoty = []
	for line in f:
		item = {'pozice': pozice, 'mt_mereni_id': idcko}
		# nacist delky
		m = re.match("\s*LC\s+=\s+([0-9\.]+)\s+([0-9\.]+)\s+([0-9\-\.]+)\s+([0-9\-\.]+)\s+([0-9\-\.]+)\s*", line, re.I|re.U)
		if m <> None:
			# print "match LC" 
			try:
				parametr = pole2id['LC_'+str(poradi_delka)]
				item['tolerance_nazvy_id'] = parametr
			except KeyError:
				pass
			else:
				# projit a zkusit najit
				found = False
				for idx in range(len(mt_hodnoty)):
					# pokud najdeme pridame do pole
					if mt_hodnoty[idx]['tolerance_nazvy_id'] == parametr:
						found = True
						mt_hodnoty[idx]['namereno'].append(m.group(1))
						break
				if not found:
					item['namereno'] = [m.group(1)]
					item['nominal'] = m.group(2)
					item['tol_max'] = m.group(4)
					item['tol_min'] = m.group(5)
					mt_hodnoty.append(item)
			poradi_delka += 1
			continue

		# nacist uhly
		m = re.match("\s*CA\s+=\s+([0-9]+\s{1,2}[0-9]{1,2}\'\s?[0-9]{1,2}\")" + \
			"\s+([0-9\-]+\s{1,2}[0-9]{1,2}\'\s?[0-9]{1,2}\")" + \
			"\s+([0-9\-]+\s{1,2}[0-9]{1,2}\'\s?[0-9]{1,2}\")" + \
			"\s+([0-9\-]+\s{1,2}[0-9]{1,2}\'\s?[0-9]{1,2}\")" + \
			"\s+([0-9\-]+\s{1,2}[0-9]{1,2}\'\s?[0-9]{1,2}\")", line, re.I|re.U)
		if m <> None:
			# print "match CA" 
			try:
				parametr = pole2id['CA_'+str(poradi_uhel)]
				item['tolerance_nazvy_id'] = parametr
			except KeyError:
				pass
			else:
				# projit a zkusit najit
				found = False
				for idx in range(len(mt_hodnoty)):
					# pokud najdeme pridame do pole
					if mt_hodnoty[idx]['tolerance_nazvy_id'] == parametr:
						found = True
						mt_hodnoty[idx]['namereno'].append(m.group(1))
						break
				if not found:
					item['namereno'] = parse_uhel(m.group(1))
					item['nominal'] = parse_uhel(m.group(2))
					item['tol_max'] = parse_uhel(m.group(4))
					item['tol_min'] = parse_uhel(m.group(5))
					mt_hodnoty.append(item)
			poradi_uhel += 1
			continue

		# dosli jsme na konec dat jednoho kusu
		if re.match("[\-]{10,}\s+[\-]{10,}\s+", line, re.I|re.U) <> None:
			poradi_uhel = 1
			poradi_delka = 1
			pozice += 1
			# dopocitat prumery
			for item in mt_hodnoty:
				item['namereno'] = sum(map(Decimal, item['namereno']))/len(item['namereno'])
				tabulky.mt_hodnoty.insert(item)
			mt_hodnoty = []
	# abychom nezapomneli vlozit posledni pozici
	if len(mt_hodnoty) > 0:	
		for item in mt_hodnoty:
			item['namereno'] = sum(map(Decimal, item['namereno']))/len(item['namereno'])
			tabulky.mt_hodnoty.insert(item)

	print "ok"

def parse_uhel(txt):
	m = re.match("([0-9\-]+)\s{1,2}([0-9]{1,2})\'\s?([0-9]{1,2})\"", txt, re.I|re.U)
	if m == None:
		return None
	else:
		return Decimal(m.group(1)) + Decimal(m.group(2))/60 + Decimal(m.group(3))/3600

# prochazeni adresaru se skripty 
# arg - seznam, do ktereho se ukladaji soubory nebo
#     - funkce, ktera se vola nad kazdym souborem
def walk_dir(arg, dirname, names):
	if names == None:
		os.path.walk(dirname, walk_dir, arg)
	else:
		for item in names:
			name = os.path.join(dirname, item)
			if os.path.isdir(name):
				os.path.walk(name, walk_dir, arg)
			elif callable(arg):
				arg(name)
			else:
				arg.append(name)

if __name__ == "__main__":
	t = Tabulky()
	t.mt_mereni.begin()
	if os.path.isfile(sys.argv[1]):
		parse_data(t, sys.argv[1])
	elif os.path.isdir(sys.argv[1]):
		files = []
		walk_dir(files, sys.argv, None)
		for f in files:
			parse_data(t, files)
	t.mt_mereni.commit()
		
