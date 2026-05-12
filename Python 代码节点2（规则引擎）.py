def main():
    try:  # ← 在这里开始 try 块
        import json
        
        text = params.get("query", "")
        
        HARD_BAN_WORDS = [
            "免费票", "盘前票", "公开票", "免费分享", "盘前公开", "盘后验证",
            "内部票", "内部股", "龙头股", "金股", "涨停战法",
            "一票赚", "封仓", "领涨股", "人气股",
            "暴涨", "疯涨", "飙涨", "大赚", "怒赚", "狂赚", "马后炮",
            "机密", "绝密", "核心机密", "加密发布", "内部绝密", "高度机密",
            "知根知底", "了如指掌", "特批", "帮扶价", "抢筹",
            "我发誓", "毒誓", "我确保", "我以人格担保", "帮不到你势不罢休",
            "没骗你", "骗你是小狗", "骗你被车撞", "骗你跳黄浦江", "中国人不骗中国人",
            "全体备战", "稳赚", "实盘",
            "完美避险", "规避所有风险", "避开下跌", "无惧调整",
            "抵御熊市", "锁定风险", "绝对安全", "低风险无回撤",
            "大幅降低亏损", "行情差也能稳赚", "系统性避险",
            "无脑操作", "不用思考", "坐等收益", "代替人工决策",
            "全网第一", "行业第一",
            "精准荐股", "合法荐股", "告别亏损", "摆脱被套", "不再亏钱",
            "打败散户", "碾压手动操作", "淘汰传统炒股",
            "散户必亏", "手动操作注定亏损", "历史表现复刻", "往期收益可复制","量化系统",
        ]
        
        HARD_BAN_PHRASES = [
            "服务费不会让您白花", "有好的收获",
            "人无横财不富", "马无夜草不肥",
            "饿死胆小的", "撑死胆大的",
            "爽不爽", "刺激不刺激",
        ]
        
        PRODUCT_VIOLATIONS = [
            ("量化系统", "树懒"),
            ("量化交易系统", ""),
            ("量化软件", ""),
            ("交易系统", "树懒"),
        ]
        
        hits = []
        for w in HARD_BAN_WORDS:
            if w in text:
                if w == "封仓" and ("容量" in text or "策略" in text):
                    continue
                if w == "实盘" and "客户" in text:
                    continue
                hits.append(w)
        
        for p in HARD_BAN_PHRASES:
            if p in text:
                hits.append(f"[话术] {p}")
        
        if hits:
            return {
                "verdict": "VIOLATION",
                "status": "blocked",
                "reason": f"命中硬禁止词: {', '.join(hits)}",
                "hits": hits
            }
        
        pv_hits = []
        for kw, exempt in PRODUCT_VIOLATIONS:
            if kw in text:
                if exempt and exempt in text:
                    continue
                pv_hits.append(kw)
        
        if pv_hits:
            return {
                "verdict": "VIOLATION",
                "status": "blocked",
                "reason": f"命中产品称谓违规: {', '.join(pv_hits)}",
                "hits": pv_hits
            }
        
        return {
            "verdict": "PASS_ENGINE",
            "status": "needs_ai",
            "reason": "规则引擎放行，提交AI审核",
            "hits": []
        }
    
    except Exception as e:  # ← 在这里捕获所有异常
        return {
            "verdict": "ERROR",
            "status": "error",
            "reason": f"规则引擎执行出错: {str(e)}",
            "hits": []
        }