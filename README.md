# MLLM
Evaluation of Multi-modal Large Language Models <br />
## LVLMs 
| Rank |                            Model                             |                           Version                            |    VanillaEval    |  Triple-check   |
| :--: | :----------------------------------------------------------: | :----------------------------------------------------------: | :---------: |:---------: |
|  1   | **[InternLM-XComposer2-VL](https://github.com/InternLM/InternLM-XComposer)** | **[InternLM2-7B](https://github.com/InternLM/InternLM-XComposer)** | **57.88** | **41.59** |
|  2   |      [mPLUG-Owl2](https://arxiv.org/pdf/2311.04257.pdf)      | [LLaMA2-7B](https://github.com/X-PLUG/mPLUG-Owl/tree/main/mPLUG-Owl2) |   49   |   7.19   |
|  3   |  [LLaVA](https://arxiv.org/pdf/2304.08485.pdf)         |      [Vicuna-13B](https://github.com/haotian-liu/LLaVA)      |   42.97   |  19.72   |
|  4   |        [MoE-LLaVA](https://arxiv.org/pdf/2401.15947.pdf)       |   [Phi-2.7B×4](https://github.com/PKU-YuanGroup/MoE-LLaVA)   |   41.65   |   21.63   |
|  5   |  [IDEFICS](https://huggingface.co/blog/idefics)  |     [Llama-65b](https://huggingface.co/HuggingFaceM4/idefics-80b-instruct)     |   41.02   |   3.67   |
|  6   |       [MiniCPM-V](https://github.com/OpenBMB/MiniCPM/#minicpm-v)   | [MiniCPM-2B](https://github.com/OpenBMB/MiniCPM/#minicpm-v)  |   39.93   |  5.32   |
|  7   | [InternLM-XComposer-VL](https://github.com/InternLM/InternLM-XComposer) | [InternLM-7B](https://github.com/InternLM/InternLM-XComposer) |   38.53   |  1.15   |
|  8  | [VisCpm](https://arxiv.org/pdf/2308.12038.pdf) | [CPMBee-10B](https://github.com/OpenBMB/VisCPM) |   36.51   |  0.9   |
|  9  |    [BLIP-2](https://arxiv.org/pdf/2301.12597.pdf)        | [Flant5xxl](https://github.com/salesforce/LAVIS/tree/main/projects/blip2) |   36.24   |  0.5   |
|  10  |    [MMICL](https://arxiv.org/pdf/2309.07915.pdf)         |        [FlanT5xxl](https://github.com/HaozheZhao/MIC)        |   34.85   |  4.15   |
|  11  |  [Qwen-VL-Chat](https://github.com/QwenLM/Qwen-VL/)      |         [Qwen-7B](https://github.com/QwenLM/Qwen-VL)         |   34.72   |  9.04   |
|  12  |           [CogVLM](https://arxiv.org/pdf/2311.03079.pdf)        |         [Vicuna-7B](https://github.com/THUDM/CogVLM)         |   33.59   |  4.93   |
|  13  |[InstructBLIP](https://arxiv.org/pdf/2305.06500.pdf)     | [FlanT5xxl](https://github.com/salesforce/LAVIS/tree/main/projects/instructblip) |   33.45   |  0.1   |
|  14  |      [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B)     |    [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B)     |   29.39    |  1.67   |
|  15  |        [mPLUG-Owl](https://arxiv.org/pdf/2304.14178.pdf)       | [LLaMA-7B](https://huggingface.co/MAGAer13/mplug-owl-llama-7b) |   26.72    |  0.1   |
## Tasks
<br />
## Datasets
*[Our Dataset](https://drive.google.com/file/d/17MI7m0JO0xOyIQu1IYwI5RNqSI2shrh6/view?usp=sharing)*. <br />

## Run
```
python run.py --model [LVLM] --task [Task]
```
