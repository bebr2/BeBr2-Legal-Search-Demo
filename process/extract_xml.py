# encoding: utf-8
'''
提取XML文件中的数据，每个文件存在一个json里
一个json的例子：
{
    "text": "浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号 原告：韦斌姬，女，1972年9月22日出生，汉族，住东阳市。 被告：韦斌强，男，1969年6月17日出生，汉族，住东阳市。 被告：杜满萍，女，1968年11月25日出生，汉族，住东阳市。 委托代理人：陈菊华、贾凌珂。 原告韦斌姬为与被告韦斌强、杜满萍民间借贷纠纷一案，于2016年12月1日向本院提起诉讼，请求判令两被告归还借款10万元，并支付利息（自起诉之日起按中国人民银行同期同档次贷款基准利率计算至实际履行之日止）。本院受理后，依法由审判员甘震适用简易程序独任审判。被告杜满萍在提交答辩状期间对管辖权提出异议，本院裁定予以驳回。杜满萍不服该裁定，上诉至金华市中级人民法院。后金华市中级人民法院驳回上诉，维持原裁定。2017年4月20日，被告杜满萍申请对借条中“杜满萍”的签名是否系其本人书写进行鉴定，本院依法委托金华天鉴司法鉴定所进行鉴定。本院于2017年7月6日公开开庭审理了本案。原告韦斌姬、被告韦斌强及被告杜满萍的委托代理人贾凌珂到庭参加了诉讼。本案现已审理终结。 本院经审理查明：2011年4月25日，被告韦斌强、杜满萍向原告韦斌姬借款10万元，并共同出具了借条一份，内容为：“今向韦斌姬借人民币拾万元正。”庭审中，原告韦斌姬自认被告杜满萍已归还款项2.4万元，其余款项未归还。被告韦斌强陈述其分文未还。被告杜满萍陈述其对案涉借款不知情，故分文未还。在本案审理过程中，被告杜满萍申请对借条中“杜满萍”的签名是否系其本人书写进行鉴定，本院依法委托金华天鉴司法鉴定所进行鉴定，鉴定意见为借条落款处的“杜满萍”的签名字迹与杜满萍样本字迹系同一人书写形成。 本院依照《中华人民共和国合同法》第二百零六条、第二百零七条之规定，判决如下： 一、被告韦斌强、杜满萍于本判决生效之日起十日内归还原告韦斌姬借款7.6万元，并支付利息（自2016年12月1日起按中国人民银行公布的同期同档次贷款基准利率计算至实际归还之日止）。 二、驳回原告韦斌姬的其他诉讼请求。 如果被告未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。 案件受理费2300元，减半收取1150元，由原告韦斌姬负担276元，由被告韦斌强、杜满萍负担874元；鉴定费3200元（已由被告杜满萍预交），由被告杜满萍负担。 如不服本判决，可在本判决书送达之日起十五日内向本院递交上诉状，并按对方当事人的人数提出副本，上诉于浙江省金华市中级人民法院。 审判员甘震 二〇一七年七月七日 代书记员许天瑶 ",
    "title": "浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号 ",
    "wszzdw": "法院",
    "fywszl-wszl": "裁判文书",
    "jbfy-cbjg": "浙江省东阳市人民法院",
    "wsmc": "判决书",
    "ah": "（2016）浙0783民初17571号",
    "ajlx-ajlb": "民事一审案件",
    "province": "浙江",
    "city": "金华市",
    "year": "2017",
    "reason": [
        "民间借贷纠纷"
    ],
    "ajlbsimple": "民事",
    "ft": [
        "中华人民共和国合同法"
    ]
}
'''

import os
import xml.etree.ElementTree as ET
import json
import re
import tqdm

data_path = "../data/Legal_data"
output_path = "../data/processed"

name_list = ["wszzdw", "fywszl-wszl", "jbfy-cbjg", "wsmc", "ah", "ajlx-ajlb"]
wsmc_list = set()

wsmc_type = ["判决书", "裁定书", "决定书", "通知书", "调解书"]
ajlb_type = ["民事", "行政", "赔偿", "刑事", "执行"]
province = ["最高", "广东", "山东", "江苏", "河南", "浙江", "四川", "湖北", "湖南", "河北", "福建", "上海", "北京", "陕西", "云南", "广西", "安徽", "海南", "江西", "重庆", "辽宁", "天津", "黑龙江", "山西", "内蒙古", "新疆", "贵州", "甘肃", "吉林", "青海", "宁夏", "西藏", "香港", "澳门", "台湾"]

# 可能是儿子节点或孙子节点的处理
def myfind(root, name):
    try:
        return root.find(f".//{name.upper()}").attrib['value']
    except:
        return None

# 提取法律名字，书名号里的内容
def extract_ft(root):
    fts = root.findall('.//FT')
    laws = set()
    if not fts:
        return None
    for ft in fts:
        try:
            laws.add(re.findall('《(.*)》', ft.attrib["value"])[0])
        except:
            pass
    return list(laws) if laws else None

# 提取中文年份为阿拉伯数字
def extract_year(root):
    try:
        content = root.findall('./WW')[0].attrib['value']
        pattern = r'([〇一二三四五六七八九]{4})年'
        match = re.search(pattern, content)
        if match:
            year_chinese = match[1]
            return str(
                int(
                    year_chinese.translate(
                        str.maketrans("〇一二三四五六七八九", "0123456789")
                    )
                )
            )
        else:
            return None
    except:
        return None

# 提取XML文件中的数据，传入参数为tree
def extract(tree):
    root = tree.getroot()

    WS = root[0].findall('./WS')[0]
    data = {"text": root[0].attrib['oValue'], "title": WS.attrib['value']}
    for name in name_list:
        # 对于有'-'的，尝试前面部分，如果没有，尝试后面部分
        if '-' in name:
            try:
                data[name] = WS.find(name.split('-')[0].upper()).attrib['value']
            except:
                data[name] = myfind(WS, name.split('-')[1].upper())
        else:
            if name == "wsmc" or name == "ah":
                data[name] = myfind(WS, name.upper())
            else:
                data[name] = WS.find(name.upper()).attrib['value']
        if name == "wsmc" and data["wsmc"] is None:
            for wsmc in wsmc_list:
                # 在tree中找到有没有value为wsmc的节点
                if tree.findall(f".//*[@value='{wsmc}']"):
                    data["wsmc"] = wsmc
                    break
    # 可能在孙子节点，可能在儿子节点
    data["province"] = myfind(WS, 'XZQH_P')
    if data["province"] is None:
        try:
            data["province"] = re.findall('[\u4e00-\u9fa5]+省', data["title"])[0]
        except:
            pass
    data["city"] = myfind(WS, 'XZQH_C')
    try:
        AH = WS.findall('./AH')[0]
        data["year"] = AH.find('LAND').attrib['value']
        if not (data["year"].startswith("19") or data["year"].startswith("20")) or len(data["year"]) != 4:
            data["year"] = extract_year(root[0])
    except:
        data["year"] = extract_year(root[0])
    try:
        data["reason"] = tree.findall(".//WZAY")[0].attrib['value'].split("、")
    except:
        data["reason"] = None
    wsmc_list.add(data["wsmc"])
    # 将data["wsmc"]中简化为wsmc_type中的字样，如果找不到置为None
    if data["wsmc"] is not None:
        data["wsmc"] = next(
            (
                wsmc_type_item
                for wsmc_type_item in wsmc_type
                if wsmc_type_item in data["wsmc"]
            ),
            None,
        )
    # 将ajlx-ajlb中简化为ajlb_type中的字样，如果找不到置为其他，如果本身是None，置为None
    if data["ajlx-ajlb"] is not None:
        data["ajlbsimple"] = next(
            (
                ajlb_type_item
                for ajlb_type_item in ajlb_type
                if ajlb_type_item in data["ajlx-ajlb"]
            ),
            "其他",
        )
    else:
        data["ajlbsimple"] = None
    # 精细化处理省份名字
    if data["province"] is not None:
        data["province"] = next(
            (
                province_item
                for province_item in province
                if province_item in data["province"]
            ),
            None,
        )
    data["ft"] = extract_ft(root)
    return data
    
    

if __name__ == "__main__":
    names = os.listdir(data_path)
    failed_num = 0
    for name in tqdm.tqdm(names):
        try:
            tree = ET.parse(os.path.join(data_path, name))
        except:
            print(name)
            failed_num += 1
            continue
        with open(os.path.join(output_path, f"{name[:-4]}.json"), 'w', encoding='utf-8') as f:
            json.dump(extract(tree), f, ensure_ascii=False, indent=4)
    print(f"Finished, failed_num: {failed_num}")
        
        