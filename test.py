sub_features = {'高額現金回饋': [{'title': '國內現金回饋', 'payload': 'in'},
                                {'title': '國外現金回饋', 'payload': 'out'}],
                '旅遊交通': [{'title': '里程累積', 'payload': 'meter'},
                            {'title': '旅遊優惠', 'payload': 'travel'},
                            {'title': '國外刷卡優惠', 'payload': 'outside'},
                            {'title': '高鐵', 'payload': 'hsr'},
                            {'title': '加油停車', 'payload': 'oil'},
                            {'title': 'eTag', 'payload': 'etag'}],
                '休閒娛樂': [{'title': '美食', 'payload': 'food'},
                            {'title': '電影', 'payload': 'movie'}],
                '購物': [{'title': '通路聯名', 'payload': 'chain'},
                        {'title': '網路購物', 'payload': 'shopee'}]
                }

message = '高額現金回饋'

if message in sub_features:
    print(sub_features[message])