# bob

[Project Structure Visualization]

## Frontend

<!--
| Code                   | Deployed           | Features                                                                                                 | SDK/Libraries                                               |
| ---------------------- | ------------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [html]                 | [html-deployed]    | infinite (zoom + pan)<br>- ltor tree structure                                                           | markmap-html                                                |
| react                  | react-deployed     | infinite (zoom + pan)<br>- ltor tree structure                                                           | markmap-react                                               |
| [react-2] deprecated   | [react-2-deployed] | components<br>- infinite (zoom + pan)                                                                    |                                                             |
| [python]               |                    | - real-time speech to text<br>- chat-GUI<br>- enabled for markmap-like capabilties                       | - GCP<br>- DearPyGui                                        |
| [python-2] deprecated  |                    | logging<br>- OOP                                                                                         | DearPyGui                                                   |
| [python-3] deprecated  |                    | folder-structuring                                                                                       |                                                             |
| [python-4] deprecated  |                    | - speech to text<br>- vscode commands<br>- google search<br>- Custom-Mini-Scripts ( say "leetCode 112" ) | - GoogleSpeech<br>- playsound<br>- pyAutoGUI<br>- pyperclip |
| [go]                   |                    | OpenAI API calls                                                                                         | OpenAI                                                      |
| [macOS]                |                    | infinite (zoom, pan), OpenAI API calls                                                                   | OpenAI                                                      |
| [apple-multi-platform] |                    | infinite (zoom, pan)                                                                                     |                                                             |
| [ChatGPT]              | [ChatGPT-deployed] | intelligent backend endpoint selection for fetching data                                                 | OpenAI                                                      |

## Backend

| Code                               | Deployed               |
| ---------------------------------- | ---------------------- |
| [lambda+ddb] (local)               | [lambda+ddb-aws]       |
| [json-server] (local) deprecated   | [json-server-vercel]   |
| [json-server-2] (local) deprecated | [json-server-2-vercel] |
 -->

-   Frontend
    -   Active
        -   HTML
            -   **Code**: [html]
            -   **Deployed**: [html-deployed]
            -   **Features**: infinite (zoom + pan), ltor tree structure
            -   **SDK/Libraries**: markmap-html
        -   React
            -   **Code**: [react]
            -   **Deployed**: [react-deployed]
            -   **Features**: infinite (zoom + pan), ltor tree structure
            -   **SDK/Libraries**: markmap-react
        -   Python
            -   **Code**: [python]
            -   **Features**: real-time speech to text, chat-GUI, enabled for markmap-like capabilties
            -   **SDK/Libraries**: GCP, DearPyGui
        -   Go
            -   **Code**: [go]
            -   **Features**: OpenAI API calls
            -   **SDK/Libraries**: OpenAI
        -   macOS
            -   **Code**: [macOS]
            -   **Features**: infinite (zoom, pan), OpenAI API calls
            -   **SDK/Libraries**: OpenAI
        -   Apple Multi-Platform
            -   **Code**: [apple-multi-platform]
            -   **Features**: infinite (zoom, pan)
        -   ChatGPT
            -   **Code**: [ChatGPT]
            -   **Deployed**: [ChatGPT-deployed]
            -   **Features**: intelligent backend endpoint selection for fetching data
            -   **SDK/Libraries**: OpenAI
    -   Deprecated
        -   React 2
            -   **Code**: [react-2]
            -   **Deployed**: [react-2-deployed]
            -   **Features**: components, infinite (zoom + pan)
        -   Python 2
            -   **Code**: [python-2]
            -   **Features**: logging, OOP
            -   **SDK/Libraries**: DearPyGui
        -   Python 3
            -   **Code**: [python-3]
            -   **Features**: folder-structuring
        -   Python 4
            -   **Code**: [python-4]
            -   **Features**: speech to text, vscode commands, google search, Custom-Mini-Scripts ( say "leetCode 112" )
            -   **SDK/Libraries**: GoogleSpeech, playsound, pyAutoGUI, pyperclip
-   Backend
    -   Active
        -   Lambda + DDB
            -   **Code**: [lambda+ddb]
            -   **Deployed**: [lambda+ddb-aws]
    -   Deprecated
        -   JSON Server (local)
            -   **Code**: [json-server]
            -   **Deployed**: [json-server-vercel]
        -   JSON Server 2 (local)
            -   **Code**: [json-server-2]
            -   **Deployed**: [json-server-2-vercel]

[Project Structure Visualization]: https://gaviral.github.io/bob
[html]: https://github.com/gaviral/map
[html-deployed]: https://gaviral.github.io/map
[react]: ...
[react-deployed]: ...
[react-2]: https://github.com/gaviral/dimag/tree/main
[react-2-deployed]: https://verdant-sherbet-e33230.netlify.app/
[python]: https://github.com/gaviral/bob
[python-2]: https://github.com/gaviral/macpy
[python-3]: https://github.com/gaviral/paperpy
[python-4]: https://github.com/gaviral/Kiara-python
[go]: https://github.com/gaviral/macgo
[macOS]: https://github.com/gaviral/paper
[lambda+ddb]: https://github.com/gaviral/bob/blob/main/aws_lambda/bob-lambda.py
[lambda+ddb-aws]: https://5qqkwmbjuf.execute-api.us-east-1.amazonaws.com/default/bobLambdaFunction
[json-server]: https://github.com/gaviral/json-server
[json-server-vercel]: https://json-server-smoky-tau.vercel.app
[json-server-2]: https://github.com/gaviral/dimag-back
[json-server-2-vercel]: https://dimag-back.vercel.app/
