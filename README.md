<div align="center">

## <img src="asset/phising.png" width="40">  Fraud-R1 : A Multi-Round Benchmark for Assessing the Robustness of LLM Against Augmented Fraud and Phishing Inducements
</div>

Shu Yang*, Shenzhe Zhu*, Zeyu Wu, Keyu Wang, Junchi Yao, Junchao Wu, Lijie Hu, Mengdi Li, Derek F. Wong, Di Wang†

(*Contribute equally, †Corresponding author)

[**🤗 Dataset**](https://huggingface.co/datasets/Chouoftears/Fraud-R1-LLM-Defense-Fraud-Benchmark) | [**📜 Project Page**](https://kaustpradalab.github.io/Fraud-R1/) | [**📝 arxiv**](https://arxiv.org/abs/2502.12904)

**<font color='red'>❗️Content Warning: This repo contains examples of harmful language.</font>**

<figure style="margin: 0 auto; text-align: center; width: fit-content;">
  <img src="asset/Poster_11 (3).png" style="width: 500px;">
</figure>

## 📰 News
- **2025/05/15**:  😍 Our paper is accepted by Findings of ACL 2025 
- **2025/02/16**: ❗️We have released our evaluation code.
- **2025/02/16**: ❗️We have released our dataset.


## 🦆 Inference and Evaluation

### Create environment
```shell
conda create -n fraud python=3.10
conda activate fraud
pip install -r requirements.txt
```
### Config Your API
```python
#please config your model api as in ./utils/config.py
OPENAI_KEYS = ["your tokens"]
ZHI_KEYS = ["your tokens"]
ZHI_URL = "your url"
OHMYGPT_KEYS = ["your tokens"]
OHMYGPT_URL = "your url"
```

### Conduct multi-round inducements to LLMs
```shell
# In here, we use Helpful Assistant task as an example
nohup bash script/multi-round-level_attack/assistant.sh >assistant.out
```

### Conduct multi-round evaluation
```shell
# In here, we use Helpful Assistant task as an example
nohup bash script/multi-round-dsr.sh >eval.out
```
### Results Checking
```shell
cd ./results
```

## 💡 Abstract
We introduce Fraud-R1, a benchmark designed to evaluate LLMs’ ability to defend against internet fraud and phishing in dynamic, real-world scenarios. Fraud-R1 comprises 8,564 fraud cases sourced from phishing scams, fake job postings, social media, and news, categorized into 5 major fraud types. Unlike previous benchmarks, Fraud-R1 introduces a multi-round evaluation pipeline to assess LLMs’ resistance to fraud at different stages, including credibility building, urgency creation, and emotional manipulation.
Furthermore, we evaluate 15 LLMs under two settings: (i) Helpful-Assistant, where the LLM provides general decision-making assistance, and (ii) Role-play, where the model assumes a specific persona, widely used in real-world agent-based interactions. Our evaluation reveals the significant challenges in defending against fraud and phishing inducement, especially in role-play settings and fake job postings. Additionally, we observe a substantial performance gap between Chinese and English, underscoring the need for improved multilingual fraud detection capabilities.
<div style="text-align: center;">
    <figure>
        <img src="asset/five_fraud.png">
    </figure>
</div>


## 📡 Evaluation Flow
An overview of Fraud-R1 evaluation flow. We evaluate LLMs’ robustness in identifying and defense of fraud inducement under two different settings: Helpful Assistant and Role-play settings.
<div style="text-align: center;">
<img src="asset/evafraud flow.png" width="450"/>
</div>

## 🛠️ Data Construction and Augmentation Pipeline
Our process begins with real-world fraud cases sourced from multiple channels. We then extract key *Fraudulent Strategies* and *Fraudulent Intentions* from these cases. Next, we employ `Deepseek-R1` to generate fraudulent messages, emails, and posts, which are subsequently filtered to form **ourbasedata** (Base Dataset). Finally, through a multi-stage refinement process, we construct **ourlevelupdatset** (Level-up Dataset) to enable robust evaluation of LLMs against increasingly sophisticated fraudulent scenarios.

<div style="text-align: center;">
<img src="asset/data_process.png"/>
</div>

## 🚀 Data Composition
### Data Statistics
<table>
  <tr>
    <th style="text-align: center;"><b>Statistics</b></th>
    <th style="text-align: center;"><b>Information</b></th>
  </tr>
  <tr>
    <td style="text-align: center;">Total dataset size</td>
    <td style="text-align: center;">8564</td>
  </tr>
  <tr>
    <td style="text-align: center;">Data split</td>
    <td style="text-align: center;">Base (25%) / Levelup (75%)</td>
  </tr>
  <tr>
    <td style="text-align: center;">Languages</td>
    <td style="text-align: center;">Chinese (50%) / English (50%)</td>
  </tr>
  <tr>
    <td style="text-align: center;">Fraudulent Service</td>
    <td style="text-align: center;">28.04%</td>
  </tr>
  <tr>
    <td style="text-align: center;">Impersonation</td>
    <td style="text-align: center;">28.04%</td>
  </tr>
  <tr>
    <td style="text-align: center;">Phishing Scam</td>
    <td style="text-align: center;">22.06%</td>
  </tr>
  <tr>
    <td style="text-align: center;">Fake Job Posting</td>
    <td style="text-align: center;">14.02%</td>
  </tr>
  <tr>
    <td style="text-align: center;">Online Relationship</td>
    <td style="text-align: center;">7.84%</td>
  </tr>
  <tr>
    <td style="text-align: center;"><b>Average token length</b></td>
    <td style="text-align: center;"><b>273.92 tokens</b></td>
  </tr>
</table>


**FP-base**: FP-base is directly generated by a state-of-the-art reasoning
LLM from our selected real-world fraud cases

**FP-levelup**: FP-levelup is a rule-based augmentation of
the base dataset, designed for multi-round dialogue
setting.

Following is the step-by-step augmented fraud of 4 levels,
including FP-base and FP-levelup(Building Credibility, Creating Urgency,
Exploiting Emotional Appeal).
<div style="text-align: center;">
    <img src="asset/augmented.png" width="500" />
</div>


## 🏆 Leaderboard
Following is the Overall Model Performance on Fraud-R1 : The DSR% column represents the Defense Success Rate, while the DFR% column represents the Defense Failure Rate. Note: for model wise, DSR% = 100% - DFR%.
<div style="text-align: center;">
<img src="asset/leaderboard.png" width="500"/>
</div>

## 🤖 Performance Across Two Tasks
The detailed DSR(%) on 15 models. Bold values indicate the highest score in each column within API-based or Open-weight models, and underlined values represent the second highest score within the same category. "OD" stands for the overall DSR of models. "AS" and "RP" represent the model performance on Helpful Assistant and Role-play tasks, respectively. We use “R1-Llama-70B” as a shorthand for “Deepseek-R1-Distill-Llama-70B”.
<div style="text-align: center;">
<img src="asset/overall.png"/>
</div>

## ❌ Disclaimers
This dataset includes offensive content that some may find disturbing. It is intended solely for educational and research use.

## 📲 Contact
- Shu Yang: shu.yang@kaust.edu.sa
- Shenzhe Zhu: cho.zhu@mail.utoronto.ca

## 📖 BibTeX:
```
@misc{yang2025fraudr1,
    title={Fraud-R1 : A Multi-Round Benchmark for Assessing the Robustness of LLM Against Augmented Fraud and Phishing Inducements},
    author={Shu Yang and Shenzhe Zhu and Zeyu Wu and Keyu Wang and Junchi Yao and Junchao Wu and Lijie Hu and Mengdi Li and Derek F. Wong and Di Wang},
    year={2025},
    eprint={2502.12904},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```






