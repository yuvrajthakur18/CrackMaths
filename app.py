import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## Set up the Streamlit app
st.set_page_config(page_title="Text To Maths Problem Solver And Data Search Assistant", page_icon="🧮")

# Custom CSS for styling the title
st.markdown(
    """
    <style>
    .custom-title {
        border: 2px solid pink;
        background-color: blackfade;
        color: white;
        padding: 10px;
        text-align: center;
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }
    .custom-title:hover {
        transform: scale(1.1);
        color: red;
        border-color: red;
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with custom styling
st.markdown('<h1 class="custom-title">CrackMaths - Text To Maths Problem Solver.</h1>', unsafe_allow_html=True)

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

## Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the various information on the topics mentioned"
)

## Initialize the Math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression need to be provided"
)

prompt = """
You're an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation
and display it pointwise for the question below.
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combine all the tools into a chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

## Initialize the agents
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

## Let's start the interaction
question = st.text_area("Enter your question:", "A sum of Rs 53 is divided among A, B, and C in such a way that A gets Rs. 7 more than what B gets, and B gets Rs. 8 more than what C gets. What is the ratio of their shares?")

if st.button("Find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({'role': 'assistant', "content": response})
            st.write('### Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")



# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain.chains import LLMMathChain, LLMChain
# from langchain.prompts import PromptTemplate
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain.agents.agent_types import AgentType
# from langchain.agents import Tool, initialize_agent
# from langchain.callbacks import StreamlitCallbackHandler

# ## Set upi the Stramlit app
# st.set_page_config(page_title="Text To Maths Problem Solver And Data Search Assistant",page_icon="🧮")
# st.title("CrackMaths - Text To Maths Problem Solver.")

# groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


# if not groq_api_key:
#     st.info("Please add your Groq API key to continue")
#     st.stop()

# llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


# ## Initializing the tools
# wikipedia_wrapper=WikipediaAPIWrapper()
# wikipedia_tool=Tool(
#     name="Wikipedia",
#     func=wikipedia_wrapper.run,
#     description="A tool for searching the Internet to find the vatious information on the topics mentioned"

# )

# ## Initializa the MAth tool

# math_chain=LLMMathChain.from_llm(llm=llm)
# calculator=Tool(
#     name="Calculator",
#     func=math_chain.run,
#     description="A tool for answering math related questions. Only input mathematical expression need to be provided"
# )

# prompt="""
# Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
# and display it point wise for the question below
# Question:{question}
# Answer:
# """

# prompt_template=PromptTemplate(
#     input_variables=["question"],
#     template=prompt
# )

# ## Combine all the tools into chain
# chain=LLMChain(llm=llm,prompt=prompt_template)

# reasoning_tool=Tool(
#     name="Reasoning tool",
#     func=chain.run,
#     description="A tool for answering logic-based and reasoning questions."
# )

# ## initialize the agents

# assistant_agent=initialize_agent(
#     tools=[wikipedia_tool,calculator,reasoning_tool],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=False,
#     handle_parsing_errors=True
# )

# if "messages" not in st.session_state:
#     st.session_state["messages"]=[
#         {"role":"assistant","content":"Hi, I'm a Math chatbot who can answer all your maths questions"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg['content'])

# ## Lets start the interaction
# question=st.text_area("Enter your question:","A sum of rs 53 is divided among A, B and C in such a way that A gets Rs. 7 more than what B gets and B gets Rs. 8 more than what C gets. What is the ratio of their shares ?")

# if st.button("Find my answer"):
#     if question:
#         with st.spinner("Generate response.."):
#             st.session_state.messages.append({"role":"user","content":question})
#             st.chat_message("user").write(question)

#             st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
#             response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
#                                          )
#             st.session_state.messages.append({'role':'assistant',"content":response})
#             st.write('### Response:')
#             st.success(response)

#     else:
#         st.warning("Please enter the question")
