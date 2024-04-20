# LLM Prompt Recovery
<h2>Abstract</h2>
AI, and GenAI particularly in recent years, is often met with significant opposition due to our inability to understand the decision-making that goes on under the hood of the respective model. Because of this, researchers and industry professionals are racing to figure out ways to dig into the infrastructure of transformer models to incorporate reasoning traces that could potentially shed light on how we can unravel the black box inner workings of AI. This repository contains the efforts of the team KAD Solutions in the LLM Prompt Recovery Machine Learning Competition hosted by Kaggle in partnership with Google to exhibit the release of their new family of lightweight LLMs entitled Gemma between February 27th and April 16th, 2024. We fine-tuned the 2-billion parameter Gemma LLM using low-rank adaptation to build an inference LLM capable of reasoning about the most likely rewrite prompt given for an original and rewritten text pair. Overall, our team "KAD Solutions" placed in the top 40th percentile of participants with a highest-recorded testing similarity score of 0.62. <br>

<h2>Introduction</h2>

<h3>Competition</h3> 
<strong>Objective</strong>: Construct an NLP model capable of recovering the prompt likely given to a different language model used to transform an original text into the respective rewritten version. <br>
<strong>Restrictions</strong>:
<li>CPU Notebook <= 9 hours run-time </li>
<li>GPU Notebook <= 9 hours run-time</li>
<li>Internet access disabled</li>
<li>Freely & publicly available external data is allowed, including pre-trained models</li>
<strong>Evaluation Metric</strong>: The measure of success in this competition is sharpened cosine similarity of the T5 sentence embeddings taken from the predictions and actual prompts during scoring.
  
<h3>Approach</h3>
Due to the immense computational and monetary expense of training our own LLM, we knew that we would have to work with the open-source LLMs, and because the competition testing dataset consisted of texts that were rewritten using Google's Gemma model, we thought it would be a reasonable starting point for our investigation into the task. The Gemma family is a lightweight family of models ranging from 2-billion to 7-billion parameters. Astonishingly, it outperforms existing open-source models of equal or greater number of parameters like Llama 7b and 13b and Mistral 7b on benchmarks such as MMLU, HellaSwag, and HumanEval. Additionally, it does not need to be quantized to be ran on a single GPU efficiently, though it is still possible to quantize the model further and generate strong inferences. So, our approach to the initial build was to use the base Gemma 2b LLM to conduct the inference task, or in other words, have the base Gemma model try and recover the prompt without any further training or guidance, and that went as poorly as it is simplistic. 

<h3>Model Design</h3>
At this point, we knew that the base Gemma model would not be enough to conduct the inference task and we were interested in trying other pre-trained models, but regardless of model choice, we ultimately concluded it would be more important to try and inform the model about the specific task than it was trying to accomplish than to run through different open-source options. So, this led to a period of research until we found a fine-tuning method incorporated by the Keras team to fine-tune the Gemma base-model. Keras is a very popular API library that is part of the Tensorflow Python library utilized for very high-level control of machine learning pipelines. They have prebuilt commands that conduct a plethora of activity in the low-level for developers to build deep-learning infrastructures much quicker while maintaining a sizable amount of control in the low-level. This meant we could effectually "teach" the Gemma LLM how to structure its responses in order to better align with the prompts in the testing data and thereby increase testing similarity. The baseline model that we built to make sure worked consisted of the Gemma pre-trained model house in the Keras architecture so that we could insert a layer of fine-tuning using low-rank adaptation according to inform Gemma about the task through further training. 

<h3>Data Warehouse</h3>
Once we reevaluated our approach, the next objective became wrangling, cleaning and loading data for further training. Due to the growing interest in LLM codebase development throughout the tech sector, there is a vast amount of already somewhat cleaned text data available in the corners of the open-source community. So, the next step in our workflow involved constructing a data warehouse that sorted text data based on its "type". We categorized text data into 3 different categories: colloquial, declarative, interrogative, prose, fiction, nonfiction, miscellaneous Due to certain text sources fitting into multiple categories, the definitions for each category are as follows: colloquial text data represents texts that contain abbreviations, slang and acronyms that are legible to humans, but not standard for the language itself. Declarative texts are short texts that are standard in the language and make a statement that could be interpretable as fiction or nonfiction. Interrogative texts pose a question. Prose are short texts that are also standard in the language but focus on more literary or rhythmic aspects of the language. Fiction texts are long texts that contain no factually accurate plots, details or summaries. Nonfiction is the opposite: long texts that are factually accurate. Miscellaneous texts fall into no other categories like programming code or math equations. Once we had over 25 text sources warehoused and cleaned, we sampled 300 pieces from a careful distribution of our various sources to create a balanced blend of 3000 examples of different types of text. 

<h3>Data Transformation</h3>
In the next step of our build, we needed to create the dataset that would be ultimately fitted onto Gemma to better teach it about the inference objective. In order to create that dataset, we put together a 300-example list of rewrite prompts, generated mostly by ChatGPT and our own design. This list was split to include 150 examples without proper nouns and 150 examples with proper nouns. Admittedly, there are likely more optimized approaches to aligning rewrite prompts with original texts and that represents something that we will circle back to in future directions for the optimization of the inference model. These 300 examples were set up to be randomly chosen from when each original from the blend is given to Gemma to rewrite. In other words, all of the original texts were randomly paired with one of the 300 prompts from the list and then Gemma rewrote that text according to the prompt. After about 14 hours of GPU runtime, Gemma had generated 3000 rewritten versions for our 3000 original examples along with the 3000 random selections for rewrite prompts. 

<h3>Fitting & Submitting</h3>
In order for fine-tuning to make a little bit more sense, I want to zoom out and share a little bit of background on transformer models and LLMs in particular. LLMs are the applications of transformer models in the context of NLP. Transformer models are specialized models that can run directionally and still retain an attentional mechanism. Prior to 2017, machine learning applications need both an encoding module and a decoding module communicating data back and forth. With the development of the transformer model, either submodule (encoder or decoder) could function independently and retain information as each stage of the machine learning task progressed. So, pretrained LLMs have already spent hundreds of hours embedding trillions of words into a vector space and repositioning those embeddings/"words" to create a rich, intelligent correlational memory for the significance of words. You can think of this in your own intellectual progression. Throughout grade school, we spend time learning and strengthening the vocabulary, semantics, grammar and syntax of our native languages. Then, we fine-tune our concept of language in later years to the contexts that we are immersed in. For example, people typically do not use the same language in a business conference as they do at a sporting event or social gathering. 


Circling back to the topic of our individual model, when we fine-tune the model using low-rank adaptation we are actively repositioning where all of the billion parameters for tokens in the models vocabulary are in order to increase the model's chances of outputting words that resemble the training data during fine-tuning. So, when we fit the curated blend of text data onto our Keras-Gemma model, we leverage the Keras architecture to conduct deep-learning of the curated training data under the hood of Gemma's base model. This means that the weakly correlated inferences of the base model are strengthened by the examples in that 300-example list of prompts that we use to rewrite the total 3000 examples. Put plainly, we are aligning Gemma's predictive capacity with the task objective, to the best of our knowledge. 

However, when we finally submitted our model to be ran on the testing data for the competition, we had a significant realization when our model scored an 0.51 in similarity. We had created a very strong, general-purpose prompt inference model as evidenced by the 0.7 for the training accuracy, but that did not directly translate to high similarity score with the testing data because Kaggle intentionally hid the test dataset from all participants. So, although we had a sufficiently well-fit general-purpose model, in order to increase our score, we would want to overfit the model to the Kaggle testing data which would mean probing the hidden testing corpus for trends and quirks that we could incorporate in our fine-tuning blend to instead teach the model how to output prompts like those in the competition. This was a sweeping conclusion reached by the Kaggle community of participants in this competition, which ultimately ushered in participants that were testing a singular rewrite prompt to compare with all of the actual prompts, coined the mean prompt. Strong mean prompts included "Improve this text" and longer versions of that sentiment. 

<h3>Concluding Thoughts</h3>
Throughout the discussion of this competition, the inability to see the type of data that participants needed to optimize for proved to be a large critique of the competition itself. Our team was able to optimize an inference model to output predictions upwards of 0.6 in cosine similarity and the winning team in the competition was able to reach 0.71, but no team progressed above that benchmark by the conclusion of the competition. This takes us back to the age old saying "garbage in, garbage out". We had successfully created a very strong prompt-recovering LLM for our 300 example list of prompts, but there were only so many ways to probe the testing data for improvements that we could make fine-tune our model so as to overfit the testing corpus. For example, ensuring that the model limited the rewrite prompt to succinct, single sentence command that did not feature direct mentions to the text yield more correlative inferences. In the real world, it is absolutely possible for rewrite prompts to be multiple sentences or feature different syntax from the data we used in training, thus isolating the competition from its grandiose purpose. Unfortunately, the Kaggle community came to the consensus that this was too grand a limitation for the competition itself; however, we feel as though Google and Kaggle were aware of the sheer difficulty of the task and is directly reflected by the $200,000 in cash prizes to the top 7 teams in the competition. Fine-tuning LLMs has a significant effect on the text generation ability of LLMs as long as you understand the volume and type of data needed to sufficiently inform your LLM. Otherwise, it becomes very difficult because zero-shot and few-shot reasoning tasks are still very advanced abilities for LLMs and the Gemma family is restricted due to its lightweight size. We can confidently assert after having participated in this competition that Google's Gemma family is very impressive, but it is still a ways behind the proprietary LLMs like ChatGPT that shocked the world, and understandably so. ChatGPT has 175 billion token parameters, whereas Gemma's biggest model has 7 billion. We expect Google to continue to try to optimize lightweight models so as to make them easier for the open-source community to interact with, but on the flip side, Google's Gemma family also teaches us that lightweight models have the potential to radically change the data science scene. Gemma will not be the last open-model designed by Google, but it represents a very strong stepping stone into advanced, lightweight LLMs for easy production deployment. In reading the discussion of the top competitor's project, we discovered he scored best by conducting an adversarial attack on the testing data to discover a text string "lucrera" that increases the similarity score as its repeated up until a point. So, from a human perspective, they are the least similar prompts imaginable to the actuals, but the evaluation metric is being exploited by an attacker AI probe. 

<h3>Key Takeaways</h3>
<li>Gemma is a very advanced, yet limited lightweight LLM that deserves further investigation.</li>
<li>Fine-tuning LLMs is a really effective method at utilizing pretrained models for niche use-cases.</li>
<li>The cosine similarity of T5 sentence embeddings is an easily-manipulable metric for comparing similarity of two texts.</li>
<li>LLMs are not inherently scary, but instead need to be better developed so as to be smarter than the adversarial attacks which render them to the control of the attacker.</li>
