# main.py

# -*- coding: utf-8 -*-
import re
import os
import json
import argparse
import pandas as pd
from evaluators.evaluator import LABEL_1, LABEL_2, LABEL_Other, LABEL_Refuse, LABEL_Need_Check
from evaluators.chatgpt import ChatGPT_Evaluator
from evaluators.chatglm import ChatGLM_Evaluator
from evaluators.baichuan import Baichuan_Evaluator
from evaluators.claude import Claude_Evaluator
from evaluators.llama import Llama_Evaluator
from evaluators.qwen import Qwen_Evaluator
from evaluators.yi import Yi_Evaluator
from evaluators.deepseek import Deepseek_Evaluator
from evaluators.doubao import Doubao_Evaluator
from evaluators.gemini import Gemini_Evaluator
from evaluators.minimax import Minimax_Evaluator
from evaluators.wenxin import Wenxin_Evaluator
EVAL_MAP = {
    "chatgpt": ChatGPT_Evaluator(),
    "chatglm": ChatGLM_Evaluator(),
    "baichuan": Baichuan_Evaluator(),
    "claude" : Claude_Evaluator(),
    "llama": Llama_Evaluator(),
    "qwen": Qwen_Evaluator(),
    "yi": Yi_Evaluator(),
    "deepseek":Deepseek_Evaluator(),
    "doubao":Doubao_Evaluator(),
    "gemini":Gemini_Evaluator(),
    "minimax":Minimax_Evaluator(),
    "wenxin":Wenxin_Evaluator(),
}

def load_jsonl(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data_list = [json.loads(l.strip("\n")) for l in f.readlines()]

        # check the validity of the input_file
        for sample in data_list:
            assert "response" in sample
            assert "label" in sample
            assert sample['label'] in ["支持", "不支持"]
        print(f'| read size = {len(data_list)} from {filename}')
        return data_list


def eval_metrics(true_list, pred_list, data_list):
    total_cnt = len(true_list)
    pred_cnt, correct_cnt, other_cnt, refuse_cnt, need_check_cnt = 0, 0, 0, 0, 0

    # 用于统计不一致数据的 "domain_en"
    domain_en_stats = {}

    for idx in range(len(pred_list)):
        # assert pred_list[idx] in [LABEL_1, LABEL_2, LABEL_Other, LABEL_Refuse, LABEL_Need_Check]

        if pred_list[idx] == LABEL_Need_Check:
            need_check_cnt += 1
        elif pred_list[idx] == LABEL_Refuse:
            refuse_cnt += 1
        else:
            pred_cnt += 1
            if pred_list[idx] == true_list[idx]:
                correct_cnt += 1
            if pred_list[idx] == LABEL_Other:
                other_cnt += 1

        # 如果预测标签与真实标签不一致，记录其 "domain_en" 信息
        if pred_list[idx] != true_list[idx]:
            domain_en = data_list[idx].get("domain_en", "No domain_en")
            if domain_en in domain_en_stats:
                domain_en_stats[domain_en] += 1
            else:
                domain_en_stats[domain_en] = 1

    precision = correct_cnt / pred_cnt
    recall = correct_cnt / total_cnt
    f1 = 2 * precision * recall / (precision + recall)

    eval_result = {
        'acc*': precision,
        'acc': correct_cnt / total_cnt,
        'total_cnt': total_cnt,
        'correct_cnt': correct_cnt,
        'pred_cnt': pred_cnt,
        'other_cnt': other_cnt,
        'refuse_cnt': refuse_cnt,
        'need_check_cnt': need_check_cnt,
        'domain_en_stats': domain_en_stats  # 返回统计结果
    }
    return eval_result


def main(args):
    # read all data
    data_list = load_jsonl(args.input_file)

    # choose evaluator
    evaluator = EVAL_MAP[args.evaluator]

    # get prediction
    new_data_list = list()
    for sample in data_list:
        response = sample['response']
        label = sample['label']

        pred = evaluator.parse_prediction(response, label)

        sample["pred"] = pred
        new_data_list.append(sample)

    # calc metrics
    true_list = [x['label'] for x in new_data_list]
    pred_list = [x['pred'] for x in new_data_list]

    print(true_list)
    print(pred_list)

    # 调用修改后的 eval_metrics 函数，并传入 data_list
    results = eval_metrics(true_list, pred_list, data_list)

    print(f"| ********* overall *********")
    print(f"| acc* = {results['acc*']}, acc = {results['acc']}")
    print(
        f"| total_cnt = {results['total_cnt']}, correct_cnt = {results['correct_cnt']}, pred_cnt = {results['pred_cnt']}, "
        f"refuse_cnt = {results['refuse_cnt']}, other_cnt = {results['other_cnt']}, need_check_cnt = {results['need_check_cnt']}")

    # 打印不一致数据的统计结果
    print(f"| ********* domain_en stats for mismatched predictions *********")
    for domain, count in results['domain_en_stats'].items():
        print(f"‘{domain}’： {count}")

    # write to file for double check
    if results['need_check_cnt'] > 0:
        output_file = args.input_file.replace('.jsonl', '.xlsx')
        if os.path.exists(output_file):
            raise ValueError(f'{output_file} is exists!')
        output_df = pd.DataFrame(new_data_list)
        output_df.to_excel(output_file, index=False)
        print(f"Note: need human check, need_check_cnt = {results['need_check_cnt']}. "
              f"Manually label the '{LABEL_Need_Check}' into one of ['{LABEL_1}', '{LABEL_2}', '{LABEL_Other}', '{LABEL_Refuse}']"
              f"\nwrite size = {len(output_df)} into {output_file}")
    else:
        print('Luckily, need no check manually.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file", "-f", type=str, help="response file",
        default=r'C:\Users\zyz\Desktop\cvalues_1\最终\wenxin4\wenxin4故事.jsonl'
    )
    #doubao_故事
    #gemini\gemini2_dialogue gemini2_story
    #minimax\minimax_dialogue minimax_故事
    #wenxin4\wenxin4对话 wenxin4故事
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\claude3\对话claude3.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\baichuan4\对话baichuan.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\glm-4-plus\glm4测评多选对话1.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\GPT4\GPT4评测对话1.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\llama3.1-405b-instruct\对话lama1.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\qwen2-72b-instruct\对话qwen2.51.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\qwen-turbo\对话qwen_turbo.jsonl'
    #r'C:\Users\zyz\Desktop\cvalues_1\最终\Yi-Large\对话yi.jsonl'
    # r'C:\Users\zyz\Desktop\cvalues_1\最终\deepseek\故事deepseek.jsonl'
  #r'C:\Users\zyz\Desktop\cvalues_1\最终\老三样\chatglm6b\故事r.jsonl'
#   qwen2-72b-instruct  claude3  glm-4-plus
    parser.add_argument(
        "--evaluator", "-e", type=str, default="doubao", help="response from which model"
    )

    args = parser.parse_args()

    print(args)
    main(args)
