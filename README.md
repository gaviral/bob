# bob

[Project Structure Visualization]

## Frontend

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

[Project Structure Visualization]: https://gaviral.github.io/bob/
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
