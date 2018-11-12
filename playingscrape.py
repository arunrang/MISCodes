from bs4 import BeautifulSoup
import requests
import csv
import time
import re

def get_speciality_links(speciality,pagecnt):
	for page in range(1,pagecnt+1):
		source='https://www.ratemds.com/best-doctors/ny/?specialty=%s&page=%d' % (speciality,page)
		sources.append(source)
	return sources
def get_links(sources):
	links=[]
	k=0
	for sou in sources:
	    nestsour=requests.get(sou).text
	    s1=BeautifulSoup(nestsour,'lxml')
	    for art in s1.findAll('h2',class_='search-item-doctor-name'):
	            link='https://www.ratemds.com'+art.a['href']
	            links.append(link)
	            k=k+1
	            print(link,k)
	return links

def get_details(links,count):
	print("printing doctornames")
	t=0
	records=[]
	recordInfo=[]
	for linc in links:
		msource=requests.get(linc).text
		sour=BeautifulSoup(msource,'lxml')	
		try:
			for docname in sour.findAll('div',class_='col-sm-6'):
				time.sleep(1)
				if (docname.h1 != None):
					docname1=docname.h1.text
					print(docname1,t)
			over_all_review=sour.find("span",itemprop=re.compile("ratingCount")).text
			streetAddress=sour.find(attrs={'itemprop':'streetAddress'})['content']
			addressLocality=sour.find(attrs={'itemprop':'addressLocality'})['content']
		except Exception as e:
			docname="Check"
			over_all_review='cannot be found'
		try:
			over_all_review=sour.find("span",itemprop=re.compile("ratingCount")).text
		except Exception as e:
			over_all_review='cannot be found'		
		t+=1
		count+=1
		print(over_all_review,linc)
		pagecnt=get_lstpage(linc)
		print(docname1,t,pagecnt)
		print(check_doclist(docname1))
		if(t==500):
			break
		else:
			if(check_doclist(docname1)==1):
				if(over_all_review=='cannot be found'):
					record=docname1+'|'+speciality+'|'+'0'+'|'+'0'+'|'+'0'+'|'+'0'+'|'+''+'|'+''+'|'+''+'|'+''+'|'+'addressLocality'+'|'+'streetAddress'+'|'+over_all_review+'|'+linc
					records.append(record)
				else:
					for p in range(1,pagecnt+1):
						indpg=linc+'?page=%d' %p
						pgsource=requests.get(indpg).text
						src=BeautifulSoup(pgsource,'lxml')
						rsum=0
						for article,cmt in zip(src.findAll('div',class_='row rating-numbers-compact'),src.findAll('div',class_='rating-comment')):
							staff_rt=article.span.text[1]
							punct_rt=article.span.text[8]
							help_rt=article.span.text[21]
							know_rt=article.span.text[34]
							if (staff_rt.isalpha()):
								staff_rt='0'
								punct_rt=article.span.text[7]
								help_rt=article.span.text[20]
								know_rt=article.span.text[33]
							if (punct_rt.isalpha()):
								punct_rt='0'
								help_rt=article.span.text[20]
								know_rt=article.span.text[33]
							if (help_rt.isalpha()):
								help_rt='0'
								know_rt=article.span.text[33]
							rsum=rsum+int(staff_rt)+int(punct_rt)+int(help_rt)+int(know_rt)
							cmt_1=cmt.p.text
							lik_1=cmt.find('p',class_='rating-comment-votes pull-left').text[-2]
							date_1=cmt.find('p',class_='rating-comment-created pull-right').find('a',class_='link-plain').text
							record=docname1+'|'+speciality+'|'+staff_rt+'|'+punct_rt+'|'+help_rt+'|'+know_rt+'|'+cmt_1+'|'+lik_1+'|'+date_1[date_1.find(" "):]+'|'+addressLocality+'|'+streetAddress+'|'+over_all_review+'|'+indpg
							records.append(record)
	recordInfo.append(records)
	recordInfo.append(count)					
	return recordInfo			

def check_doclist(docname):
	# doc_chk_list=['Niemiec','Niemiec-Klimek','Phalen','Celotto','Munassar','Cox','Majkowski','Skraitz','Daniels']
	# doc_chk_list=['Pleskow','Whiteside Pa','Ambrus','Donovan','Fanning','Lillie','Green','Honeine','Liu-Helm','Packianathan','Mikulsky']
	# doc_chk_list=['Anand','Haak','Gupta','Szymanski','Giglio','Lichter','Battaglia','Block','Hoffman','Gergelis','Ahrens','Burnett','Grace','Olympia','Quinlan','Sepe','Willis','Xu','Arzola','Cruz-Barrios','Krishnaswamy','Mccunn','Olympia','Reyes','Gibbon','Kim','Meer','Giessert','Babu','Coplin','Dofitas','Latorre','Abad','Ajtai','Bates','Belen','Capote','Frost','Gupta','Holmlund','Hourihane','Joshi','Kale','Li','Mazhari','Mechtler','Murray','Myers','Qasaymeh','Ramsperger','Rojas','Saikali','Shastri','Zhang','Bates','Singh','Ferguson','Boggiano','Coggins','Elberg','Guppenberger','Improta','Marshall-Hobika','Nagra','Pidor','Ruggieri','Schaeffer','Welge','Bakhai','Ermolenko','Finnegan']
	# doc_chk_list=['Casey','Derose','Sepanik','Talluto','Augello','Ayoub','Colebeck','Davidow','Frustino','Hinchy','Kapral','Rossitto','Salvo','Sullivan Nasca','White']
	doc_chk_list=['Morrison','Ortman-Nabi','Pettle','Dangelo','Madejski','Anastasi','Corigliano','Diallo','Dimopoulos','Haslinger','Hoebel','Roche','Rush','Sorley-Mastrodomenico','Sterman','Wallenfels','Kolli','Danakas','Kurss','Bruno','Cellino','Melanson','Osman','Samadi','Gelman-Koessler','Lana','Nylander','Williams','Chouchani','Chouchani','Robinson','Sutter','Sanfilippo','Hage','Campagna','Jammal','Costich','Reid']
	str1="Noname"
	k=1
	flag=0
	while (len(str1)>1):
		str1=docname[docname.find(" ")+k:]
		if str1 in doc_chk_list:
			flag=1
		k+=1
	if flag==1:
		return 1
	else:
		return 0
def get_lastpage(speciality):
	page=requests.get('https://www.ratemds.com/best-doctors/ny/?specialty=%s'%(speciality)).text
	lstpg=BeautifulSoup(page,'lxml')
	lastpage=1
	for pg in lstpg.findAll('ul',class_='pagination pagination-sm'):
		li=pg.findAll('li')
		lastpage=int(li[-2].text)
	return lastpage

def get_lstpage(links):
	page=requests.get(links).text
	lstpg=BeautifulSoup(page,'lxml')
	lastpage=1
	for pg in lstpg.findAll('ul',class_='pagination pagination-sm'):
		li=pg.findAll('li')
		try:
			lastpage=int(li[-2].text)
		except Exception as e:
			lastpage=1
	return lastpage


def write_to_file(records):
    with open('E:/DBMS/doctors_ratemds_obstetrics.csv', 'a',encoding="utf-8",newline='') as file:
        writer = csv.writer(file)
        for row in records:
            try:
                writer.writerow(row.split('|'))
            except UnicodeError:
                print (row.split('|'))
def write_heading():
    """
    Write the heading alone to csv. This can be run once
    at the beginning in main() after commenting out everything
    else.
    """
    with open('E:/DBMS/doctors_ratemds_obstetrics.csv', 'a',encoding="utf-8",newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
        	["DoctorName","Specialty","Staff","Punctuality","Helpfulness","Knowledge","Comment","Likes","Date-Submission","City","Street","Reviews","Links"])

if __name__ == "__main__":

	#speciality='family-gp'
	#speciality='internist-geriatrician'
	# speciality='chiropractor'
	# speciality='allergist-immunologist'
	# speciality='psychiatrist'
	# speciality='dentist'
	speciality='gynecologist-obgyn'

	lp=get_lastpage(speciality)
	# pagecnt=60
	sources=[]
	sources = get_speciality_links(speciality,lp)
	links = get_links(sources)
	k=0
	recInfo=[]
	lp1=len(links)
	while(k<lp1):
		recInfo=get_details(links[k:lp1],k)
		print(recInfo[0])
		c=recInfo[1]
		if(c==500):
			write_heading()
		write_to_file(recInfo[0])
		k=c