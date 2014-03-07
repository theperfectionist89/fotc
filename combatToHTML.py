import io, re

f = open('combatHTML.txt', 'w')
f2 = open('combatOutputTest.txt', 'r')
output = f2.read()
lines = output.split('\n')

table1 = '<td><span class="stattext">'
table2 = '<td><span class="stattext" style="margin-left: 1px;">'
table3 = '</span></td>'
tableRow = '</tr><tr>'
height = 250
name1 = re.match('(\w+)',lines[1]).group(1)
name2 = re.match('(\w+)',lines[13]).group(1)

f.write('[dohtml]<center><div class="overall"><table width="440"><tr><td colspan="4"><div class="cardname2" style="background-color: #402121;"><font color="#f1f1f1">')
f.write(lines[1] + ' vs ' + lines[13])
f.write('</font></div></td></tr><tr><td colspan="4" rowspan="3"><div class="template"><div style="height:2px;"></div><table cellpadding="0" cellspacing="0"><tr><td width="250"><div class="questinfo">')
f.write(lines[1])
f.write('</div></td><td width="250"><div class="questinfo" style="margin-left: 1px;">')
f.write(lines[13])
f.write('</div></td></tr><tr><td><div class="questinternal" style="height: ')
f.write(str(height) + 'px; overflow: auto; text-align: justify; padding: 4px;"><center><i><font size="2">')
f.write(lines[2])
f.write('</font></i><br><br><br><table cellpadding="0"><tr>')

for i in range(3,6):
	stat = lines[i].split()
	f.write(table1)
	for k in range(0,3):
		f.write(stat[k])
		f.write(table3)
		if k < 2:
			f.write(table2)
	if i < 5:
		f.write(tableRow)
	else:
		f.write('</tr></table>')

f.write('</center><br><br><b><i>Perks</b></i><ul>')

buf = re.search('\[(.*)?]',lines[6])
buffs = buf.group(1).split(', ')
for b in buffs:
	f.write('<li>')
	f.write(" ".join(re.findall('[A-Z]+[a-z]*',b)))
f.write('</ul>')

f.write('<b><i>Attacks</b></i><ul>')
att = re.search('\[(.*)?]',lines[9])
attack = att.group(1).split(', ')
for a in attack:
	f.write('<li>')
	f.write(a)
f.write('</ul>')

f.write('<b><i>Powers</b></i><ul>')
pow = re.search('\[(.*)?]',lines[7])
powers = pow.group(1).split(', ')
for p in powers:
	f.write('<li>')
	f.write(" ".join(re.findall('[A-Z]+[a-z]*',p)))
f.write('</ul>')

f.write('<b><i>Buffs</b></i><ul>')
act = re.search('\[(.*)?]',lines[8])
active = act.group(1).split(', ')
for a in active:
	f.write('<li>')
	f.write(a)
f.write('</ul>')

f.write('</div></td><td><div class="questinternal" style="height:')
f.write(str(height))
f.write('px; overflow: auto; text-align: justify; padding: 4px;"><center><i><font size="2">')
f.write(lines[14])

f.write('</font></i><br><br><br><table cellpadding="0"><tr>')

for i in range(15,18):
	stat = lines[i].split()
	f.write(table1)
	for k in range(0,3):
		f.write(stat[k])
		f.write(table3)
		if k < 2:
			f.write(table2)
	if i < 17:
		f.write(tableRow)
	else:
		f.write('</tr></table>')

f.write('</center><br><br><b><i>Perks</b></i><ul>')
buf = re.search('\[(.*)?]',lines[18])
buffs = buf.group(1).split(', ')
for b in buffs:
	f.write('<li>')
	f.write(" ".join(re.findall('[A-Z]+[a-z]*',b)))
f.write('</ul>')

f.write('<b><i>Attacks</b></i><ul>')
att = re.search('\[(.*)?]',lines[21])
attack = att.group(1).split(', ')
for a in attack:
	f.write('<li>')
	f.write(a)
f.write('</ul>')

f.write('<b><i>Powers</b></i><ul>')
pow = re.search('\[(.*)?]',lines[19])
powers = pow.group(1).split(', ')
for p in powers:
	f.write('<li>')
	f.write(" ".join(re.findall('[A-Z]+[a-z]*',p)))
f.write('</ul>')

f.write('<b><i>Buffs</b></i><ul>')
act = re.search('\[(.*)?]',lines[20])
active = act.group(1).split(', ')
for a in active:
	f.write('<li>')
	f.write(a)
f.write('</ul>')

f.write('</div></td></tr></table>')

roundText = '<br><br><center><div class="stats4">Round #'
roundClose = '</div></center><div style="height:4px;"></div>'
combat = lines[25:]
rounds = []
s = ""
flag = False
for r in combat:
	if r[0:1] == " ":
		s += "&nbsp;&nbsp;&nbsp;"
		flag = True
	else: 
		if flag:
			s += "<br>"
		flag = False
	
	if r == "":
		continue
	elif r == "Endgame":
		rounds.append(s)
		s = ""
	else:
		if r != "End Round":
			s += r
			s += "<br>"
		if r == "End Round" or r[:4] == "Draw" or combat[-1] == r:
			rounds.append(s)
			s = ""
		elif "tried to run" in r or "healed" in r or "cured" in r or "fled" in r:
			s += "<br>"
	
endgame = rounds[-1]
def addBreak(matchObj):
	s = matchObj.group(0)
	return re.sub('<br>','<br><br>',s)
	
endgame = re.sub(name1 + '.*?<br>' + name2, addBreak, endgame)
 
rounds = rounds[:-1]
round = 1
for data in rounds:
	f.write(roundText)
	f.write(str(round))
	f.write(roundClose)
	f.write(data)
	round += 1

f.write('<br><br><center><div class="stats4">Endgame</div></center> <div style="height:4px;"></div>')
f.write(endgame)
f.write('</div></div></td></tr></table></div></center>[/dohtml]')
f.close()