import requests
import simplejson
import sys

def damage(atk, dfd_list):  # calculating the damage effect of an attacking type (atk) to defending types (dfd_list) 
	uri = 'http://pokeapi.co/api/v1/type/' + atk[31:]  #extracts the id of type
	r = requests.get(uri)
	content = simplejson.loads(r.text)

	damage = 1
	for key, value in content.items():
		if key=='ineffective':
			for dfdtype in value:
				if dfdtype['resource_uri'][13:] == dfd_list[0][31:] : # compare the type id's
				#	print('ineffective:', atk[31:], dfd_list[0][31:])
					damage = damage * 0.5
				if dfdtype['resource_uri'][13:] == dfd_list[1][31:] :
				#	print('ineffective:', atk[31:], dfd_list[1][31:])
					damage = damage * 0.5
		if key=='no_effect':
			for dfdtype in value:
				if dfdtype['resource_uri'][13:] == dfd_list[0][31:] :
				#	print('no_effect:', atk[31:], dfd_list[0][31:])
					damage = damage * 0.0
				if dfdtype['resource_uri'][13:] == dfd_list[1][31:] :
				#	print('no_effect:', atk[31:], dfd_list[1][31:])
					damage = damage * 0.0
		if key=='super_effective':
			for dfdtype in value:
				if dfdtype['resource_uri'][13:] == dfd_list[0][31:] :
				#	print('super_effective:', atk[31:], dfd_list[0][31:])
					damage = damage * 2
				if dfdtype['resource_uri'][13:] == dfd_list[1][31:] :
				#	print('super_effective:', atk[31:], dfd_list[1][31:])
					damage = damage * 2
					
	return damage
	
# actual program starts here
p1= sys.argv[1] 
p2= sys.argv[2] 

null_str = 'https://pokeapi.co/api/v2/type/NULL/'

uri = 'https://pokeapi.co/api/v2/pokemon/' + p1 # to get types of pokemon 1
r = requests.get(uri)

types1 = []
if r.status_code == 200:
	content = simplejson.loads(r.text)
	stat1 = content['stats'][0]['base_stat']
	for type in content['types']:
		types1.append ( type['type']['url'] )   # types are in this form: https://pokeapi.co/api/v2/type/12/
	if len(types1)==1:
		types1.append(null_str)

uri = 'https://pokeapi.co/api/v2/pokemon/' + p2 # to get types of pokemon 2
r = requests.get(uri)

types2 = []
if r.status_code == 200:
	content = simplejson.loads(r.text)
	stat2 = content['stats'][0]['base_stat']
	for type in content['types']:
		types2.append ( type['type']['url'] )
	if len(types2)==1:
		types2.append(null_str)
		
# calculate damages
damage1 = damage(types1[0], types2)
if types1[1] != null_str :  # if there is a second type
	damage12 = damage(types1[1], types2)
	damage1 = max(damage1, damage12)

damage2 = damage(types2[0], types1)
if types2[1] != null_str :
	damage22 = damage(types2[1], types1)
	damage2 = max(damage2, damage22)

# outputs
#print('damage:', damage1, damage2)
#print('stat:', stat1, stat2)
if damage1 == damage2:
	if(stat1 >= stat2):
		print(p1)
	else:	
		print(p2)
elif damage1 > damage2:
	print(p1)
else:
	print(p2)


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			