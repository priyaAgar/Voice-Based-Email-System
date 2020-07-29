# coding: utf-8

# In[3]:


import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter("ignore")   #not print matching warnings
import smtplib              #to send mail to any internet machine  (client session object)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def pdff(g): #saving plots to pdf file using matplotlib
    fig = plt.figure()
    matplotlib.pyplot.title("Doctor's Prescription For : %s" % (g.Name.iloc[0]), loc='center', color='r', fontsize=14,
                            fontweight='bold')
    ax = fig.add_subplot(111)
    text = []
    for row in range(len(g)):
        text.append(g.iloc[row])
    ax.table(cellText=text, colLabels=g.columns, loc='center')
    ax.axis('off')

    pdf = matplotlib.backends.backend_pdf.PdfPages("Your_prescription.pdf")
    pdf.savefig(fig)
    pdf.close()


def em():# sending the file via email
    fromaddr = "agarwalpriyanshi27@gmail.com"
    toaddr = "agarwalpriyanshi27@gmail.com"

    msg = MIMEMultipart()     #multipurpose internet mail extensions
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "REPORT"
    body = "PFA"
    msg.attach(MIMEText(body, 'plain'))

    filename = "Your_prescription.pdf"
    attachment = open("C:/Users/priya agarwal/Your_prescription.pdf", "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "taarey01")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


d = {'Name': [], 'Age': [], 'Gender': [], 'Disease': [], 'Prescription': [], 'Test': []}
df = pd.DataFrame(columns=d)
d1 = {1: 'Name', 2: 'Age', 3: 'Gender', 4: 'Disease', 5: 'Prescription', 6: 'Test'}
df1 = df.copy()

No_of_patients = 1
c = 0
while (True):
    if c == No_of_patients:
        break
    print()
    print('Patient No :', c)
    print()
    import speech_recognition as sr

    r = sr.Recognizer()
    for i in range(1, 7):
        with sr.Microphone() as source:
            print(d1[i], end=':')
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, 3, 3)
            try:
                text = r.recognize_google(audio)
                df[d1[i]] = [text]
                print(text)

            except Exception as e:
                print('Didn\'t recognize what you said')
    df1 = pd.concat([df1, df])
    pdff(df)
    em()
    df.drop([0], axis=0, inplace=True)
    c = c + 1

df1.to_csv('Records.csv', index=False)#Write DataFrame to a comma-separated values (csv) file

