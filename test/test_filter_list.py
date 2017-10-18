items = [
{
    'name': 'eugene',
    'type': 'asian',
},
{
    'name': 'shawn',
    'type': 'asian',
},
{
    'name': 'rob',
    'type': 'white',
}
]

filter(lambda i: i.get('type') == 'white', items)

filter_items = []
for i in items:
    if i.get('type') == 'white':
        filter_items.append(i)