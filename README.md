# LLM Prompt Recovery
<h2>Abstract</h2>
AI, and GenAI particularly in recent years, is often met with significant opposition due to our inability to understand the decision-making that goes on under the hood of the respective model. Because of this, researchers and industry professionals are racing to figure out ways to dig into the infrastructure of transformer models to incorporate reasoning traces that could potentially shed light on how we can unravel the black box inner-workings of AI. This repository contains the efforts of the team KAD Solutions in the LLM Prompt Recovery Machine Learning Competition hosted by Kaggle in partnership with Google to exhibit the release of their new family of lightweight LLMs entitled Gemma between February 27th and April 16th, 2024. We fine-tuned the 2-billion parameter Gemma LLM using low-rank adaptation to build an inference LLM capable of reasoning about the most likely rewrite prompt given for an original and rewritten text pair. Overall, our team "KAD Solutions" placed in the top 40th percentile of participants with a highest-recorded testing similarity score of 0.62. <br>

<h2>Introduction</h2>

<h3>Competition</h3> 
<strong>Objective</strong>: Construct an NLP model capable of recovering the prompt likely given to a different language model used to transform an original text into the respective rewritten version. <br>
<strong>Restrictions</strong>:
<li>CPU Notebook <= 9 hours run-time </li>
<li>GPU Notebook <= 9 hours run-time</li>
<li>Internet access disabled</li>
<li>Freely & publicly available external data is allowed, including pre-trained models</li>
  
<h3>Approach</h3>

