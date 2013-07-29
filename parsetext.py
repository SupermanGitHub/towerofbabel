# -*- coding: utf-8 -*-
import urllib
import codecs
import re
from bs4 import BeautifulSoup

def testfunc(queryWord):
  # load the web page
  url=u"http://starling.rinet.ru/cgi-bin/morph.cgi?flags=undnnnnp&root=config&word="+queryWord.lower()
  html_doc=urllib.urlopen(url.encode('utf8'))

  # create the soup
  mysoup=BeautifulSoup(html_doc)

  # print page to screen
  #print (mysoup)

  # check the type of the word (noun,verb,adjective,...)
  
  # find the td tags
  res=mysoup.find_all(['td'])
  if res==[]:
    return ""
  
  #for item in res:
    #text=''.join(item.findAll(text=True))
    #data=text.strip()
    #print data
    
  # make a list for the different word forms
  WordForms=[]

  # find the first h2 tag
  res_inf=mysoup.find_all('h2')
  if res_inf != []:
    res_inf=mysoup.find_all('h2')[0]
    infinitive=res_inf.previousSibling
    infinitive=infinitive.strip()
    #print infinitive
    # append the infinitive to the list
    WordForms.append(infinitive)
    
  for item in res:
    WordForms.append(item.string)

  for item in WordForms:
    if item == None:
      continue
    
    checkList=item.split('//')

    if len(checkList) == 1:    
      noAccent=re.sub(u'[\"\']','',checkList[0])
      #print noAccent
      #print queryWord
      if noAccent == queryWord.lower():
        position=checkList[0].find('\'')
        position_jo=checkList[0].find('\"')
        if position > -1:
          #print "Found word: " + checkList[0]
          #print "Accented vowel: " + checkList[0][position-1]
          return checkList[0]
        elif position_jo > -1:
          #print "Found word: " + checkList[0]
          #print "Accented vowel: " + checkList[0][position-1]
          return checkList[0]
        else:
          print "No accent found in word: " + checkList[0]
    else:
      noAccent=re.sub(u'[\"\']','',checkList[0])
      #print noAccent
      #print queryWord
      if noAccent == queryWord.lower():
        position=checkList[0].find('\'')
        position_jo=checkList[0].find('\"')
        if position > -1:
          #print "Found word: " + checkList[0]
          #print "Accented vowel: " + checkList[0][position-1]
          return checkList[0] + "," + checkList[1]
        elif position_jo > -1:
          #print "Found word: " + checkList[0]
          #print "Accented vowel: " + checkList[0][position-1]
          return checkList[0] + "," + checkList[1]
        else:
          print "No accent found in word: " + checkList[0]           
      
  # return the empty string if we did not find the word
  return ""      

def processBook(myBook):
  bookLines=myBook.splitlines()

  f=codecs.open('output/result.txt','w','utf8')
  #line = bookLines[3]
  ## split line into words
  #words=line.split()
  #newWords=[]
  #for item in words:
    #print item
    #res=re.sub(u"[\u2013,.!?]+","",item)
    #if len(res) > 0:     
      #accentedWord = testfunc(res)
      #if accentedWord != "":
        ##print accentedWord
        #accentedPhrase=re.sub(res,accentedWord,item)
        #newWords.append(accentedPhrase)
      #else:
        #print "Word not found"
        #newWords.append(item)
    #else:
      #newWords.append(item)

  #print "------------------Word list------------------"
  #for item in newWords:
    #print item

  #print "|--Sentence--|"
  #myLine=" ".join(newWords)
  #print myLine
  #f.write(myLine + u"\n")
  #f.close()
  

  for line in bookLines:
    # split line into words
    words=line.split()
    newWords=[]
    for item in words:
      #print item
      res=re.sub(u"[\u2013,.!?]+","",item)
      if len(res) > 0:
        accentedWord = testfunc(res)
        if accentedWord != "":
          #print accentedWord
          accentedPhrase=re.sub(res,accentedWord,item)
          newWords.append(accentedPhrase)
        else:
          #print "Word not found"
          newWords.append(item)
      else:
        newWords.append(item)

    #print "------------------Word list------------------"
    #for item in newWords:
      #print item

    myLine=" ".join(newWords)
    print myLine
    f.write(myLine + u"\n")

  f.close()    
        
def main():
  bookFile="text/text.txt"
  f=codecs.open(bookFile,'r','utf8')
  book=f.read()
  processBook(book)
    
if __name__ == "__main__":
  main()
  
  



