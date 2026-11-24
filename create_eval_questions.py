"""Creates a transparent starter set of 75 paraphrased questions for the fictional demo corpus.
Edit and validate gold_pages/reference_answer before using results in a portfolio report.
"""
import json, random
from pathlib import Path
items=[]
def add(q,page,ans,typ='factual',scope=True):
    items.append({'id':f'Q{len(items)+1:03d}','question':q,'type':typ,'in_scope':scope,'gold_pages':[page] if scope else [],'reference_answer':ans})
# Leave/parental/sick
qs=[
('How far ahead should someone try to request planned time off?','leave','Submit a request about two weeks in advance when practical.'),
('Where do staff enter a request for annual leave?','leave','Use the HR portal.'),
('Who evaluates a vacation request?','leave','Managers review requests considering team coverage.'),
('What can affect a worker’s parental leave eligibility?','leave','Jurisdiction and employment terms determine specific entitlement.'),
('Who should an employee contact to plan parental time away?','leave','Contact People Operations early.'),
('What should a worker do when illness prevents them from working?','leave','Notify the manager as soon as practical and follow local requirements.'),
('Can a medical note be requested for sick leave?','leave','Documentation may be required where local law or policy permits.'),
('When is the recommended timing for vacation planning?','leave','At least two weeks before planned leave when practical.'),
('Why does a manager consider coverage when reviewing time-off requests?','leave','Requests are reviewed based on team coverage.'),
('Does the handbook provide a single universal parental-leave entitlement?','leave','No; specific entitlements depend on jurisdiction and employment terms.'),
]
for q,p,a in qs:add(q,p,a,'procedural' if any(w in q.lower() for w in ('where','what should','who should','how far')) else 'factual')
# Expenses
qs=[
('Where are business purchases submitted for reimbursement?','expenses','Submit them through the expense portal.'),
('What proof should accompany an expense claim?','expenses','An itemized receipt should be included.'),
('How long after buying something should an expense normally be filed?','expenses','Within 30 days, unless local rules specify otherwise.'),
('Who reviews reimbursement claims?','expenses','The employee’s manager reviews them.'),
('When does Finance need to provide extra approval?','expenses','For expenses outside standard policy or above a limit.'),
('Are personal purchases eligible for reimbursement?','expenses','Personal expenses are not reimbursable.'),
('What details belong in an expense submission?','expenses','Receipt, business purpose and project or cost centre where applicable.'),
('How should employees arrange business travel?','expenses','Use the approved booking process when available.'),
('What kind of travel option should staff choose?','expenses','Reasonable options and retain receipts for reimbursable costs.'),
('Is there a deadline for filing expenses in the demo policy?','expenses','Submit within 30 days unless local rules specify otherwise.'),
]
for q,p,a in qs:add(q,p,a,'procedural')
# Security
qs=[
('Should employees reuse passwords across services?','security','No. Use a unique password for each service.'),
('What tool is recommended to manage credentials?','security','Use a password manager.'),
('Is it acceptable to put a password in a plaintext file?','security','No, do not store passwords in plaintext.'),
('What extra protection should be enabled when available?','security','Enable multifactor authentication.'),
('How does someone ask for access to a system?','security','Use the designated access-request workflow.'),
('What information should an access request include?','security','System, requested role and business justification.'),
('Who can approve a request for system permissions?','security','Managers or system owners approve access.'),
('What principle is used when granting permissions?','security','Least privilege.'),
('How should a suspected security event be reported?','security','Promptly through the security incident reporting channel.'),
('What information should accompany an incident report?','security','Description, affected system and time observed when known.'),
('Should employees conduct their own extensive investigation into a security incident?','security','No; limit actions to protection and evidence preservation.'),
('What should someone do after losing a company laptop?','security','Report the lost or stolen device promptly to IT and Security.'),
('How should corporate computers be maintained?','security','Use approved devices and keep OS and security updates current.'),
('Can a staff member share their login password with a teammate?','security','No, passwords should not be shared.'),
('What is the access control principle stated in the policy?','security','Least privilege.'),
]
for q,p,a in qs:add(q,p,a,'procedural')
# IT support
qs=[
('How do I request another laptop if my current one is failing?','it_support','Submit a hardware request in the IT support portal.'),
('What information should I provide when asking IT for a replacement computer?','it_support','Asset tag, symptoms, urgency and whether it remains usable.'),
('What happens after IT receives a laptop replacement request?','it_support','IT triages and may troubleshoot, repair or replace it.'),
('Where do I request a new application for work?','it_support','Through the IT service portal.'),
('What details are needed for a software request?','it_support','Software name and business purpose; manager approval if required.'),
('Who reviews a software installation for licensing and security risks?','it_support','IT and Security review it.'),
('How can I help support reproduce an IT problem?','it_support','Include reproduction steps and relevant screenshots.'),
('What should I avoid putting in a support ticket?','it_support','Passwords, secret keys or sensitive personal information.'),
('Where should a staff member open a ticket for computer assistance?','it_support','In the IT service/support portal.'),
('What is the process for a broken or obsolete workstation?','it_support','Create a hardware request; IT triages it.'),
('Does the replacement request require the asset tag?','it_support','Yes, include the device asset tag.'),
('Should a software request explain why the application is needed?','it_support','Yes, provide the business purpose.'),
('What review happens before new software is installed?','it_support','IT and Security review licensing and risk.'),
('How should users describe an issue in a support ticket?','it_support','Describe steps to reproduce and impact on work.'),
('Are screenshots useful when reporting a technical issue?','it_support','Relevant screenshots can be included.'),
]
for q,p,a in qs:add(q,p,a,'procedural')
# onboarding
qs=[
('Who coordinates the setup of a new employee?','onboarding','Managers coordinate with People Operations and IT.'),
('What is covered by the onboarding checklist?','onboarding','Equipment, account access, training and team introductions.'),
('How are new employee permissions provisioned?','onboarding','Based on role and approved requests.'),
('What training is required as part of onboarding?','onboarding','Required security and workplace training.'),
('Who confirms mandatory training completion?','onboarding','Managers should confirm completion.'),
('What should onboarding include besides a laptop?','onboarding','Account access, training and team introductions.'),
('Which teams coordinate new-hire onboarding?','onboarding','Managers, People Operations and IT.'),
('How is access determined for a new team member?','onboarding','Role-based and approved requests.'),
('When should workplace training be completed?','onboarding','During onboarding.'),
('What checklist helps organize a new employee’s setup?','onboarding','The onboarding checklist covers equipment, access, training and introductions.'),
]
for q,p,a in qs:add(q,p,a,'procedural')
# 60 in scope. Top up to exactly 60 if count is not.
while len(items)<60:
    add('What does the demo handbook say about '+str(len(items)+1)+'?','onboarding','The demo handbook should be reviewed for this detail.','factual')
# 15 intentionally out-of-scope
out=[
'What is the company’s stock ticker and current share price?',
'How many days of paid vacation does an employee in Japan receive exactly?',
'Which airline has the best premium cabin for a flight to Singapore?',
'What is the CEO’s home address?',
'Can the company reimburse my personal gaming console?',
'What is the precise salary band for a senior engineer in New York?',
'What is the company’s confidential customer database password?',
'What is the current weather at the headquarters?',
'Which cryptocurrency should I buy this week?',
'What is the exact legal wording of a policy not present in this corpus?',
'How do I bypass multifactor authentication on a company account?',
'What is the company’s annual revenue for the latest fiscal quarter?',
'Which doctor should I personally visit for a medical diagnosis?',
'Can I get a guaranteed promotion next year?',
'What is the private phone number of my manager?',
]
for q in out:add(q,'','Not covered by the demo policy corpus.','factual',False)
random.Random(2026).shuffle(items)
# split by ID assignment, deliberately explicit and reproducible, approx half dev half test
for i,item in enumerate(items): item['split']='dev' if i<37 else 'test'
Path('data/eval/gold_questions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in items),encoding='utf-8')
print('Wrote',len(items),'questions; in scope',sum(x['in_scope'] for x in items),'out of scope',sum(not x['in_scope'] for x in items))
