def get_file(files):
	with open(files,'r') as f:
		lines = f.readlines()
	dist = []
	reg = []
	for e in range(0,len(lines)):
		reg.append(lines[e].strip('\n').split(',')[0])
		dist.append(lines[e].strip('\n').split(',')[1])
		
	return dist,reg
	
def insert_data(files):
	from app.models import Region,District
	dist,reg = get_file(files)
	for item in range(1,len(dist)):
		regions = Region.objects.get(id = int(reg[item]))
		dis = District(region = regions,district_name = dist[item].lower())
		dis.save()
	