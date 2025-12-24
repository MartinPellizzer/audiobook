from llama_cpp import Llama

llm = None
def reply(prompt, model_filepath=''):
    global llm
    if model_filepath == '':
        model_filepath = '/home/ubuntu/vault-tmp/llm/Qwen3-8B-Q4_K_M.gguf'
    if llm == None:
        llm = Llama(
              model_path=model_filepath,
              n_gpu_layers=-1, # Uncomment to use GPU acceleration
              # seed=1337, # Uncomment to set a specific seed
              n_ctx=4096, # Uncomment to increase the context window
        )
    chat_history = []
    chat_history.append({'role': 'user', 'content': prompt})
    stream = llm.create_chat_completion(
        messages = chat_history,
        stream=True,
        temperature=0.9,
    )
    llm_response = ''
    for piece in stream:
        if 'content' in piece['choices'][0]['delta'].keys():
            response_piece = piece['choices'][0]['delta']['content']
            llm_response += response_piece
            print(response_piece, end='', flush=True)
    return llm_response

