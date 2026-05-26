## Set up a Python virtual environment

```bash
python -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

## Login NotebookLM

```bash
playwright install chromium             # ~170 MB; no progress bar — be patient (30–90 s)
notebooklm login                        # opens browser for Google sign-in
notebooklm auth check --test --json     # verify: expect "status": "ok"
```

## Start server

```bash
export notebook_id='...'
python server.py
```

## Test

Using `index.html`

## Installation service

你可以通过在终端执行以下步骤将该服务添加到系统并启动：

**1. 将服务文件复制或软链接到 systemd 目录：**
```bash
sudo cp path/to/notebooklm2openai.service /etc/systemd/system/
```

**2. 重新加载 systemd 守护进程，使其识别新服务：**
```bash
sudo systemctl daemon-reload
```

**3. 设置服务开机自启（可选）：**
```bash
sudo systemctl enable notebooklm2openai.service
```

**4. 启动服务：**
```bash
sudo systemctl start notebooklm2openai.service
```

**5. 检查服务运行状态：**
```bash
sudo systemctl status notebooklm2openai.service
```

**6. 查看服务日志输出：**
如果需要查看 server.py 打印到终端的日志，可以使用 `journalctl` 命令：
```bash
sudo journalctl -u notebooklm2openai.service -f
```