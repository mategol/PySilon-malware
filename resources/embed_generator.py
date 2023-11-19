def generate_embed(ctx, **kwargs):
    embed = discord.Embed(title=kwargs['title'], description=kwargs['description'], color=kwargs['color'])
    for cfg in kwargs.keys():
        match cfg:
            case 'fields':
                for field in kwargs['fields']: embed.add_field(name=field[0], value=field[1], inline=field[2])
            case 'thumbnail': embed.set_thumbnail(url=kwargs['thumbnail'])
            case 'footer':
                footer_text = (kwargs['footer'] if kwargs['footer'] != DEFAULT else 'PySilon Malware') if type(kwargs['footer']) != list else (kwargs['footer'][0] if kwargs['footer'][0] != DEFAULT else 'https://github.com/mategol/PySilon-malware')
                if type(kwargs['footer']) == list and len(kwargs['footer']) == 2: 
                    footer_icon = kwargs['footer'][1] if kwargs['footer'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                    embed.set_footer(text=footer_text, icon_url=footer_icon)
                else: embed.set_footer(text=footer_text)
            case 'url': embed.url = kwargs['url'] if kwargs['url'] != DEFAULT else 'https://github.com/mategol/PySilon-malware'
            case 'timestamp': embed.timestamp = kwargs['timestamp'] if kwargs['timestamp'] != DEFAULT else ctx.message.created_at
            case 'image': embed.set_image(url=kwargs['image'])
            case 'author':
                author_name = (kwargs['author'] if kwargs['author'] != DEFAULT else 'PySilon Malware') if type(kwargs['author']) != list else (kwargs['author'][0] if kwargs['author'][0] != DEFAULT else 'PySilon Malware')
                if type(kwargs['author']) == list and len(kwargs['author']) == 2: 
                    author_icon = kwargs['author'][1] if kwargs['author'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                    embed.set_author(name=author_name, icon_url=author_icon)
                else: embed.set_author(name=author_name)
    return embed
