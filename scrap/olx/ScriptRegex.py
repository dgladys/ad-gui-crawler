import json
import re

class ScriptRegex:

    def find_olx_data(self, content: str):
        result = re.findall(
            "<script type=\"text/javascript\" id=\"olx-init-config\">(.+?)</script>",
            content,
            re.MULTILINE | re.DOTALL
        )
        sc = result[0]
        vc = re.findall("window\\.__([A-Z_]+)__= (?:'|\")(.+?)(?:'|\");", sc, re.MULTILINE | re.DOTALL)
        res = {}
        for i, vt in enumerate(vc):
            n = vt[0]
            v = vt[1]
            try:
                v = v.replace('\\"', '"').replace('\\"', '"')
                p =json.loads(v)
                res[n] = p
            except json.decoder.JSONDecodeError:
                res[n] = v
        #self.save_to_file(res)
        return res
    def save_to_file(self, data):
        with open('data.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)