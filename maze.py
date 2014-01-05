import minecraft,block
import random
import sys
import time

#By mcnalu http://blog.mcnalu.net
#License GPLv3.0

#Possible improvements:
# - don't make a door in a wall that already has one
# - allow doors to be anywhere in wall
# - make exit anywhere along furthest two sides
# - make it less likely for algo to revist rooms
# - generate room structure in memory, then build maze in mc


def doorDir():
	dr=random.randint(0,3)
	if dr==0:
		dd=[1,0]
	elif dr==1:
		dd=[-1,0]
	elif dr==2:
		dd=[0,1]
	else:
		dd=[0,-1]
	return dd
	
mc=minecraft.Minecraft.create()

mc.player.setTilePos(2,1,-2)

if len(sys.argv)>1:
	isAir=True
else:
	isAir=False

if isAir==True:
	stairs=block.AIR
	stone=block.AIR
	diamond=block.AIR
	torch=block.AIR
	wool=block.AIR
	sleepTime=0
else:
	stairs=block.STAIRS_WOOD
	stone=block.STONE
	diamond=block.DIAMOND_ORE
	torch=block.TORCH
	wool=block.WOOL
	sleepTime=0

centreBlocks=[stone]*10
centreBlocks.extend([block.IRON_BLOCK,block.GOLD_BLOCK,block.DIAMOND_BLOCK])

# xs,ys,zs is tile with corner block near maze entrance
xs=0
ys=0
zs=0
height=4
#roomSize MUST be odd at present
roomSize=5
nRooms=6

#Make whole maze

#Number of blocks on each side of maze
nMaze=1+nRooms*(roomSize+1)
# xs,ys,zs is tile with corner block near maze exit
xe=xs+nMaze-1
ye=ys+height
ze=xs+nMaze-1

if xe>127 or ye>127 or ze>127:
	print 'ERROR: World size exceeded. Quitting.'

mc.setBlocks(xs,ys,zs,xe,ye,ze,stone)

if isAir==True:
	exit()

#Make handy room size parameters
r=roomSize/2
r1=1+r

# xre,zre is tile at centre of room with exit door
xre=xe-r1
zre=ze-r1

#make exit door
mc.setBlock(xre,ys+1,ze,block.AIR)
mc.setBlock(xre,ys+2,ze,block.AIR)

#Make entrance
x=xs+r1
mc.setBlock(x,ys+1,zs,block.AIR)
mc.setBlock(x,ys+2,zs,block.AIR)
z=zs+r1
#x,z is now centre of first room

nVisits=0
rooms=set()
while True:
	rIndex=((x-xs)/(1+roomSize))*nRooms+(z-zs)/(1+roomSize)
	print rIndex,x,z
	nVisits+=1
	if rIndex not in rooms:
		rooms.add(rIndex)
		#hollow out the room
		mc.setBlocks(x-r,ys+1,z-r,x+r,ys+height-1,z+r,block.AIR)
		mc.setBlock(x,ys,z,centreBlocks[random.randint(0,len(centreBlocks)-1)])
		if random.randint(0,1)==0:
			mc.setBlock(x,ys+1,z,torch)
	#quit if exit room is found
	if x==xre and z==zre:
		break
	doorFound=False
	while not doorFound:
		dd=doorDir()
		xx=x+dd[0]*r1
		zz=z+dd[1]*r1
		#if not outside wall
		if xx!=xs and zz!=zs and xx!=xe and zz!=ze:
			doorFound=True
			#make door
			mc.setBlock(xx,ys+1,zz,block.AIR)
			mc.setBlock(xx,ys+2,zz,block.AIR)
			#mc.setBlock(xx-dd[0],ys+3,zz-dd[1],torch)
			#move to centre of new room
			x=xx+dd[0]*r1
			z=zz+dd[1]*r1

print '%s rooms visited'%(nVisits)
