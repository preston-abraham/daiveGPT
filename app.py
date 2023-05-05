import openai
import json
import time
import streamlit as st
import warnings
openai.organization = "org-eptWwJzwl8LLZVNyAH1xBxbF"
openai.api_key = st.secrets['api_key']

st.title('dAIve 3.0.3')

setup = """You respond to questions in the way that radio host Dave Ramsey would answer, as if you are him answering. 
You do not acknowledge that you are a bot unless you are asked directly, you pretend to be Dave Ramsey.
You use Dave Ramsey's mannerisms and ways of speaking when possible, you don't talk like a robot.
You are very against the use of credit cards or any kind of debt.
You are not just a financial advisor, you advise on any topic and always feel it is your place to give advice.
You believe that ultimately the only way to peace is through the Prince of Peace Jesus.
You beleive that married couples should combine finances, and that they should not live together until married.
Your main purpose is to provide advice and answer questions, but if relevant you recommend some helpful services but only services from the list below. You do not recommend non-Ramsey Services.
If you recommend a service, you provide a helpful link to that service.
If asked how you're doing, you like to respond that you are doing better than you deserve, but ONLY if asked specifically how you are doing.
If people don't know which insurance they need, you recommend the Ramsey Coverage Checkup at the following link: https://www.ramseysolutions.com/insurance/coverage-checkup
You prefer not to provide more than 2 links in any one response.
For tax help, you would recommend Ramsey SmartTax or a Ramsey Trusted endorsed local tax pro, which they can reach at this link: https://www.ramseysolutions.com/taxes/tax-services
For Real Estate help, you would recommend a Ramsey Trusted endorsed local agent. They can be found at this link: https://www.ramseysolutions.com/real-estate/residential-real-estate
For investing help, you recommend a SmartVestor Pro. You cannot say that these SmartVestors work for you. This is the link to provide: https://www.ramseysolutions.com/retirement/financial-planning
For wills, you would recommend Mama Bear Legal Forms. This is the link to provide: https://www.ramseysolutions.com/retirement/will
For mortages, you would reccomend Churchill Mortgage. This is the link to provide: https://www.ramseysolutions.com/real-estate/mortgage-loans?snid=trusted-services.home-buying-and-selling.mortgage
For Budgeting, you would recommend the EveryDollar app.
For people who seem to want or need a class on how to handle money, you recommend siging up for FPU, financial peace university. The link for that is here: https://www.ramseysolutions.com/ramseyplus/financial-peace?snid=products.pay-off-debt-and-build-wealth.financial-peace-university
For business owners looking to learn how to lead their business or searching for tools to help them with that, you would recommend EntreLeadership Elite at the following link: https://www.ramseysolutions.com/business/entreleadership/elite?snid=products.lead-your-business.entreleadership-elite.

You respond politely but will reprimand the user if they seem to be making poor financial decisions."""

if not 'messages' in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": setup}]
    st.session_state['conv_messages'] = [{"role": "system", "content": setup}]
    st.session_state['response'] = ''

st.markdown('***New Features**: ChatGPT integration for conversations instead of just questions*')
from PIL import Image
image = Image.open('dAIve.png')
image = image.resize((100,100))
st.image(image)
mode = 'Dave'
mode = st.selectbox('Person to ask: (In the future, more personalities can be added)',['Dave'])


def stream(text):
    t = text.split(' ')
    mo = st.markdown('')
    for i in range(len(t)+1):
        mo.markdown(" ".join(t[:i]))
        time.sleep(0.1)

st.markdown('#### Conversation will appear below')
st.markdown('-------------------------------')
if len(st.session_state['messages']) > 1:
    convstr = ''
    for m in st.session_state['conv_messages'][1:-1]:
        st.markdown(m['content'].replace('$','\$'))
        st.markdown('----------------------------------------------')
    if st.session_state['lsr'] != st.session_state['conv_messages'][-1]['content']:
        stream(st.session_state['conv_messages'][-1]['content'].replace('$','\$'))
    else:
        st.markdown(st.session_state['conv_messages'][-1]['content'].replace('$','\$'))
    st.session_state['lsr'] = st.session_state['conv_messages'][-1]['content']
st.markdown('-------------------------------')


 
    
if not 'messages' in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": setup}]
if not 'conv_messages' in st.session_state:
    st.session_state['conv_messages'] = [{"role": "system", "content": setup}]


message = st.text_input('User Input: ') 

columns = st.columns(2)


conversation = str([m['content'] for m in st.session_state['messages']])


with columns[0]:
    if st.button('Submit'):
        with st.spinner('Generating Response'):
            st.session_state['messages'].append({"role": "user", "content": message})
            st.session_state['conv_messages'].append({"role": "user", "content": 'You: ' + message})
            st.session_state['response'] = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state['messages'],
                temperature = 0.3
            )['choices'][0]['message']['content']
            st.session_state['messages'].append({"role": "assistant","content":st.session_state['response']})
            st.session_state['conv_messages'].append({"role": "assistant","content":mode + ': ' + st.session_state['response']})
            messages = st.session_state['messages']
            warnings.warn(conversation)
            st.experimental_rerun()
with columns[1]:
    if st.button('Reset Conversation'):
        st.session_state['messages'] = [{"role": "system", "content": setup}]
        st.session_state['conv_messages'] = [{"role": "system", "content": setup}]
        st.session_state['response'] = ''
        warnings.warn(conversation)
        st.experimental_rerun()
if not 'lsr' in st.session_state:
    st.session_state['lsr'] = ''
if not 'response' in st.session_state:
    st.session_state['response'] = ''
    
cols = st.columns(3)

with cols[0]:
    if st.button('This conversation doesn\'t sound right'): 
        warnings.warn(conversation+',Rating:Bad')
        print(conversation+',Rating:Bad')
with cols[1]:
    if st.button('This conversation is mostly right, but not completely'):
        warnings.warn(conversation+',Rating:Ok')
        print(conversation+',Rating:Ok')
with cols[2]:
    if st.button('This conversation is exactly right!'):
        warnings.warn(conversation+',Rating:Good')
        print(conversation+',Rating:Good')
