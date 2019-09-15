
def cut_string(str,start,stop):
    show = ''
    for i in range(start, stop):
        show += str[i]
    return show


#person name
def correct_msg_name(name):
    #Modify the string to get the desired result
    if 'groupThread' in name:
        name = name.replace('strong', '')
        name = name.replace('span', '')
        name = name.replace('>', '')
        name = name.replace('<', '')
        name = name.replace('/', '')
        if 'img' in name:
            stop = name.find('img')
            show = cut_string(name,0,stop)
        else:
            show = name

    else:
        name = name.replace('strong', '')
        name = name.replace('span', '')
        name = name.replace('>', '')
        name = name.replace('<', '')
        stop = name.find('/')
        show = cut_string(name,0,stop)

    unread = False
    if '(' in show: #If there is unread name
        for i in range(1,11): #These lines ensure that the parentheses are actually unread messages and not in name
            if '(%s)' % i in show:
                show = cut_string(name,0,name.find('(%s)'%i)-1)
                unread = True


    if 'class' in show:
        show = cut_string(show, 0, show.find('class='))
    return show,unread

def correct_emoji(msg):
    #Emojis need their own correction

    show = ''
    while 'img alt=' in msg:
        emoji_ind = msg.find('img alt=')+9
        show += msg[emoji_ind]
        msg = cut_string(msg, emoji_ind, len(msg))
    return show


def correct_msg(msg):
    if 'img' in msg:
        return correct_emoji(msg)
    if 'GIF' in msg:
        return 'GIF'
    msg = msg.replace('<', '')
    msg = msg.replace('>', '')
    msg = msg.replace('span', '')
    msg = msg.replace('class=', '')
    start = msg.find('/')+1
    new = cut_string(msg,start,len(msg))
    new = new.replace('/', "")
    while '"' in new:
        new = cut_string(new, new.find('"')+1, len(new))



    return new


def check_sender(msg):
    sender = False
    if 'repliedLast' in msg:
        sender = True
    return sender


def combine_all(name,msg,time):
    sender = check_sender(msg)
    msg_show = correct_msg(msg)
    if sender:
        name_show = "Message to "+name
    else:
        name_show = "Message from "+name

    time_show = "Sent "+time
    print(name_show+'\n'+msg_show+'\n'+time_show)


