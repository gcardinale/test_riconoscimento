# whisper_translate_app


## Setup

You first need to download the trained model and place it in the `wevoz_model` folder.
To get the model donwload link. Please contact via email. 

You also need to add the correct token and endpoin the the `.env` file.


To build the docker image run the following command:
```bash
docker build -t  whisper_translate_app .
```

To run the docker image run the following command:
```bash
docker run  -ti  --gpus=all  -p 8005:8005 whisper_translate_app:latest
```
