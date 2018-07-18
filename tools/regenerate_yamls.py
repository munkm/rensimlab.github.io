import os
import yaml
import girder_client

rsl_page_root = os.environ.get(
    'RSL_PAGE_ROOT', '/home/xarth/codes/rensimlab/rensimlab.github.io')

collectionPath = '/collection/Renaissance Simulations'
gc = girder_client.GirderClient(apiUrl='https://girder.rensimlab.xyz/api/v1')

server_paths = yaml.load(
    open(os.path.join(rsl_page_root, '_data', 'notebooks.yaml'), 'r'))
simulation_data = yaml.load(
    open(os.path.join(rsl_page_root, '_data', 'simulations.yaml'), 'r'))

for sim_name, sim in simulation_data.items():
    for ds in sim:
        ds['on_rsl'] = False
        ds['size'] = "N/A"
    listing = gc.get('/folder/{}/listing'.format(server_paths[sim_name]))
    for folder in listing['folders']:
        try:
            pos = next((i for i, _ in enumerate(sim)
                        if folder['name'] == _['snapshot']))
            sim[pos]['on_rsl'] = folder['_id']
            sim[pos]['size'] = folder['size']
        except StopIteration:
            pass
yaml.dump(
    simulation_data,
    open(os.path.join(rsl_page_root, '_data', 'simulations.yaml'), 'w'))

rafts = [
    {'id': _['_id'], 'name': _['name'], 'description': _['description']}
    for _ in gc.get('/raft')
]
yaml.dump(
    rafts,
    open(os.path.join(rsl_page_root, '_data', 'rafts.yaml'), 'w'))