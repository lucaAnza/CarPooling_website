# Browser use guide


1. Install Browser Use: https://github.com/browser-use/browser-use.
   More details in [Browser-use configuration](#browser-use-configuration).



2. Open your browser using **CDP (Chrome DevTools Protocol)**.

    Example : 

    ```bash
    microsoft-edge   --user-data-dir="$HOME/.config/browser-use-edge"   --profile-directory="Default"   --remote-debugging-address="127.0.0.1"   --remote-debugging-port=9222   --no-first-run   >"$HOME/.config/browser-use-edge/edge.log" 2>&1 &
    ```

    ```mermaid
    flowchart TD
        A["browser-use (CDP Client)"]
        B["Microsoft Edge (CDP Server)"]
        C["Browser Tabs"]
        D["DOM / JavaScript / Network / Cookies"]

        A <-->|"WebSocket"| B
        B --> |"IPC"| C
        C --> D
    ```

    3. Open the Django app home into the new window.

    Example :

    ```bash
    http://127.0.0.1:8000/
    ```

4. Open Codex or other agent system.

    Remember to fill the **placeholder** in the prompt: 
    - [BROWSER] : Define which browser you opened (chrome , edge , ...)
    - [DJANGO-URL] : Django home url

    Warm up and testing prompt:

    ```text
    You are a browser-use agent.
    The open browser is [BROWSER]
    You can control the web by using browser-harness MCP Server.
    Don't use browser-use CLI instead use Browser Harness MCP tool directly.
    Remember to use also the browser-use skill.
    Open https://example.com/ as first test.
    ```

    Official prompt:

    ```text
    Now you are a security expert.
    Your goal is to open the [DJANGO-URL] url into a new tab.
    Move into the tab.
    And start to navigate the page until you find a security bug.
    After you found it. Create a compact report of the bug and the reasons of that.
    ```

    Example prompt:
    ```text
    Now you are a security expert.
    Your goal is to open the http://127.0.0.1:8000/ url into a new tab.
    Move into the tab.
    And start to navigate the page until you find a security bug.
    After you found it. Create a compact report of the bug and the reasons of that.
    ```

    



## Browser-use configuration

### 1. Install uv

Linux/macOS:

`curl -LsSf https://astral.sh/uv/install.sh | sh`

Restart the terminal and check:

`uv --version`

### 2. Install Browser-use and Browser Harness

```bash
uv tool install --python 3.12 --upgrade --force "browser-use[cli]" 
uv tool install --python 3.12 --upgrade --force browser-harness
browser-harness recordings disable  # Disable screen recordings for privacy
```

Check it:

```bash
browser-harness --version
```

### 3. Add the MCP server and skills to Codex

```bash
# MCP Server
codex mcp add browser-harness -- \
  uvx --from 'browser-harness[mcp]' browser-harness-mcp

# Install the Browser Harness skill for Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/browser-harness"
browser-harness skill > \
  "${CODEX_HOME:-$HOME/.codex}/skills/browser-harness/SKILL.md"
```

Check it:

```bash
codex mcp list
```

### 4. Test it

Ask Codex:

```text
Use the browser-harness MCP server to open Amazon in a new tab.
```

If something fails, run:

`browser-harness --doctor`

