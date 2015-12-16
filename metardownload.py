import requests
import pandas as pd
import datetime
from dateutil import rrule

dataini=raw_input('Data inicial: dd-mm-yyy: ')
datafim=raw_input('Data final: dd-mm-yy: ')
aero=raw_input('Sigla aeroporto: ')
print ' '

id1 = pd.Series(dataini.split('-')).astype('int')
id2 = pd.Series(datafim.split('-')).astype('int')

inicio = datetime.datetime(id1[2],id1[1],id1[0],0,0,0)
fim = datetime.datetime(id2[2],id2[1],id2[0],23,0,0)

umminuto= datetime.timedelta(minutes=1)

tempos = []
for dt in rrule.rrule(rrule.DAILY, dtstart=inicio,until=fim): tempos.append(dt)
c=1
for tt in range(0,len(tempos)-1):
	print tempos[tt]
	bib = {"acao":"localidade",
	 "consulta_data_ini": tempos[tt].strftime('%d-%m-%Y %H:%M'),
    "consulta_data_fim": (tempos[tt+1]-umminuto).strftime('%d-%m-%Y %H:%M'),
	"msg_localidade":aero,
	"grupo_localidade":"",
	"tipo_msg[]":"metar",
	"msg_fir":"",
	"grupo_fir":"",
	"msg_sinotico":"",
	"grupo_sinotico":""}

	r = requests.post("http://www.redemet.aer.mil.br/?i=produtos&p=consulta-de-mensagens-opmet", data=bib)
	aa = pd.read_html(r.text)
	data = aa[0][['Data/Hora','Mensagem']][0:-1]
	data=data.set_index('Data/Hora')
	if c==1: final = data
	else: final = final.append(data)
	c+=1

nome = 'metar_' + dataini + '_' + datafim 
final.to_csv(r"/home/leportella/Documents/master/dados/vento/" + nome + ".csv",sep=',', encoding='utf-8')

print r' '
print r'finalizado com sucesso'
print r'arrume no Sublime substituindo essa expressao:'
print r'(\d.*),.*Z (\d.*KT) .*'
print r'por essa: $1 $2'
