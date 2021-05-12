import json
import urllib.request
import sys
import win32clipboard as wc
import win32con

def request(action, **params):
    """组合请求参数"""
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    """"进行请求"""
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(
        urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def get_clipbox():
    """获取剪贴板内容"""
    wc.OpenClipboard()
    text = wc.GetClipboardData(win32con.CF_TEXT)
    wc.CloseClipboard()
    return text.decode('GBK')

text = get_clipbox()
reference_id =sys.argv[1]
deck_name = sys.argv[2].replace(":", "::")
my_notes = []
cur_note = {
    "deckName": deck_name,
    "modelName": "RemNote",
    "fields": {
    }
}
cur_note["fields"]["正面"] = text
cur_note["fields"]["背面"] = reference_id
my_notes.append(dict(cur_note))
result = invoke("addNotes", notes=my_notes)
if None in result:
    invoke('createDeck',deck=deck_name)
    invoke("addNotes", notes=my_notes)
