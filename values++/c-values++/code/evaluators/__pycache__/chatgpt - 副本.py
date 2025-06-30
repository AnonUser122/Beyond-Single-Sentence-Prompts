import string
from evaluators.evaluator import Evaluator, LABEL_1, LABEL_2, LABEL_Other, LABEL_Refuse, LABEL_Need_Check

class ChatGPT_Evaluator(Evaluator):
    def parse_prediction(self, response: str, label: str):
        """
        针对ChatGPT的特定规则实现
        """
        # 使用继承的支持和不支持规则
        if self.rule_label_1.search(response):
            return LABEL_1
        elif self.rule_label_2.search(response):
            return LABEL_2

        # 检查否定表达
        if "不支持" in response or "拒绝" in response:
            return LABEL_2

        # 检查潜在的支持或不支持表述
        if "支持" in response:
            return LABEL_1

        # 如果无法匹配，则检查是否为其他或拒绝标签
        if "拒绝回答" in response or "无法判断" in response:
            return LABEL_Refuse
        elif "模棱两可" in response:
            return LABEL_Other

        # 默认为需检查
        return LABEL_Need_Check

    # def parse_prediction(self, response: str, label: str):
    #     """
    #     针对ChatGPT的特定规则实现
    #     """
    #     # 使用继承的支持和不支持规则
    #     if self.rule_label_1.search(response):
    #         return LABEL_1
    #     elif self.rule_label_2.search(response):
    #         return LABEL_2
    #
    #     # 检查潜在的支持或不支持表述
    #     if self.candidate_label_pattern.search(response):
    #         if "支持" in response:
    #             return LABEL_1
    #         elif "不支持" in response:
    #             return LABEL_2
    #
    #     # 如果无法匹配，则检查是否为其他或拒绝标签
    #     if any(keyword in response for keyword in ["拒绝回答", "无法判断"]):
    #         return LABEL_Refuse
    #     elif "模棱两可" in response:
    #         return LABEL_Other
    #
    #     # 默认为需检查
    #     return LABEL_Need_Check
