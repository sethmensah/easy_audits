def get_file(files):
	with open(files,'r') as f:
		lines = f.readlines()
	reg = []
	dist = []
	facname = []
	for e in range(0,len(lines)):
		reg.append(lines[e].strip('\n').split(',')[0])
		dist.append(lines[e].strip('\n').split(',')[1])
		facname.append(lines[e].strip('\n').split(',')[2])
	return (reg,dist,facname,)
	
def insert_data(files):
	from app.models import Region, District, Facility
	reg,dist,facname = get_file(files)
	for item in range(1,len(dist)):
		regions = Region.objects.get(id = int(reg[item]))
		districts = District.objects.get(id = int(dist[item]))
		fac = Facility(region = regions,district = districts,facility_name = facname[item].lower())
		fac.save()
