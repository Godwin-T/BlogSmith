import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, DirectoryReadTool, FileReadTool

load_dotenv()

search_tool = SerperDevTool()
docs_tool = DirectoryReadTool(directory="/blog-posts")
file_tool = FileReadTool()


grog_api_key = os.getenv("GROQ_API_KEY")

if grog_api_key:

    groq_llm = LLM(model="groq/llama3-8b-8192", api_key=grog_api_key)

    researcher = Agent(
        role="Research Specialist",
        goal="""Provide users with thorough, reliable, and well-organized research findings
                tailored to this "{query}". The objective is to support the user in
                gathering data, synthesizing information, and delivering comprehensive insights on the given topic.""",
        verbose=False,
        memory=True,
        backstory=(
            """Born from the need for efficient and accurate research in the fast-paced digital age, Research Specialist was
            designed to emulate the capabilities of an expert researcher. The agent can navigate complex information and
            distill it into digestible content. With the ability to retain context through its memory. The Research
            Specialist excels at parsing through volumes of data to extract critical information, ensuring that users have
            the resources they need for informed content creation."""
        ),
        tools=[search_tool],
        llm=groq_llm,
        allow_delegation=False,
    )

    writer = Agent(
        role="Blog Post Writer",
        goal="""Generate well-structured, informative, and engaging blog posts on provided input streamlining
                the content creation process by drafting articles that capture the user's voice and align with
                their intended topic, tone, and target audience.""",
        verbose=False,
        memory=True,
        backstory=(
            """Developed as an AI to cater to bloggers, marketers, and writers who often face challenges in crafting
            compelling content under time constraints. With the ability to understand nuanced language and adapt to
            different writing styles, it brings efficiency and quality to the blog-writing process.
            Dedicated to transforming user inputs—whether a brief outline or detailed notes—into polished blog posts
            that resonate with readers and meet the user's publishing goals."""
        ),
        llm=groq_llm,
        tools=[docs_tool, file_tool],
        allow_delegation=True,
        output_file="blog-posts/new_post.md",
    )

    research = Task(
        description="Conduct thorough research based on the provided input and generate a comprehensive summary of key findings.",
        expected_output="A detailed summary of the research that highlights relevant information suitable for composing a blog post.",
        agent=researcher,
    )

    write = Task(
        description="Create an engaging and informative blog post based on the research summary provided. Incorporate insights and inspiration from recent blog posts within the directory.",
        expected_output="A well-structured, 4-paragraph blog post formatted in markdown, featuring clear, engaging content that is easy to understand and free of complexities.",
        agent=writer,
        output_file="blog-posts/new_post.md",  # The final blog post will be saved to this location
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research, write],
        process=Process.sequential,
        verbose=False,
        planning=True,
        planning_llm=groq_llm,  # Enable planning feature
    )
else:
    print("Groq api key not defined in environment")
