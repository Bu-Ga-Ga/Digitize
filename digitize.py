from PIL import Image
import math
#import heapq
import matplotlib.pyplot as plt


img = Image.open('1.bmp')
width, height = img.size
x = int(input('Введите начальную координату x: '))
y = int(input('Введите начальную координату y: '))
z = int(input('Введите конечную координату x: '))
r = int(input('Введите конечную координату y: '))

pixel = (x,y)
start = (x,y)
end = (z,r)
selected_color = img.getpixel((x, y))

coordinates = []

for x in range(width):
    for y in range(height):
        pixel_color = img.getpixel((x, y))
        
        if pixel_color == selected_color:
            coordinates.append((x, y))
            

def find_neighbors(pixel, coordinates):
    x, y = pixel
    neighbors = []
    remaining = set(coordinates)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor = (x + dx, y + dy)
            if neighbor in coordinates:
                if dx == 0 or dy == 0:
                    weight = 1
                else:
                    weight = math.sqrt(2)
                neighbors.append((neighbor, weight))
                remaining.discard(neighbor)
            if not remaining:
                break
        if not remaining:
            break
    if remaining:
        nearest_neighbor = None
        min_distance = float('inf')
        for coord in coordinates:
            distance = math.sqrt((x - coord[0]) ** 2 + (y - coord[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_neighbor = coord
        weight = min_distance
        neighbors.append((nearest_neighbor, weight))
    return neighbors



def find_connected_components(points):
    graph = {point: [] for point in points}


    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if (abs(points[i][0] - points[j][0]) <= 1 and abs(points[i][1] - points[j][1]) <= 1):
                graph[points[i]].append(points[j])
                graph[points[j]].append(points[i])

    components = []
    visited = set()
    for point in graph:
        if point not in visited:
            component = []
            stack = [point]
            visited.add(point)
            while stack:
                current = stack.pop()
                component.append(current)
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            components.append(component)

    return components




components = find_connected_components(coordinates)
#print(len(components))



def shortest_path(start, end, coordinates):
    queue = [(start, 0)]
    visited = {start: 0}
    path = {}
    while queue:
        current, cost = min(queue, key=lambda x: x[1])
        queue.remove((current, cost))
        if current == end:
            break
        for neighbor, weight in find_neighbors(current, coordinates):
            new_cost = visited[current] + weight
            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                priority = new_cost + math.sqrt((neighbor[0]-end[0])**2 + (neighbor[1]-end[1])**2)
                queue.append((neighbor, priority))
                path[neighbor] = current
    if end not in visited:
        return None
    current = end
    route = [current]
    while current != start:
        current = path[current]
        route.append(current)
    return list(reversed(route))



if len(components)>1:
	def find_longest_shortest_path(components):
		longest_paths = []
		for component in components:
			longest_path = []
			max_distance = 0
			for i in range(len(component)):
				for j in range(i + 1, len(component)):
					start = component[i]
					end1 = component[j]
					path = shortest_path(start, end1, component)
					if path is not None:
						distance = calculate_path_distance(path)
						if distance > max_distance and start in path or end in path:
							longest_path = path
							max_distance = distance
			longest_paths.append(longest_path)
		return longest_paths
	def calculate_path_distance(path):
		distance = 0
		for i in range(len(path) - 1):
			point1 = path[i]
			point2 = path[i + 1]
			dx = abs(point1[0] - point2[0])
			dy = abs(point1[1] - point2[1])
			if dx == 0 or dy == 0:
				distance += 1
			else:
				distance += math.sqrt(2)
		return distance



	def calculate_distance(point1, point2):
		x1, y1 = point1
		x2, y2 = point2
		return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

	def sort_coordinate_arrays(arrays, start, end):
		
		start_array = None
		for array in arrays:
			if start in array:
				start_array = array
				break
		
		if not start_array:
			return arrays
		
		sorted_arrays = [start_array]  

		current_point = start_array[-1] 
		remaining_arrays = [array for array in arrays if array != start_array]

		while current_point != end and remaining_arrays:
			closest_array = None
			closest_distance = math.inf
			for array in remaining_arrays:
				distance_to_first = math.dist(current_point, array[0])
				distance_to_last = math.dist(current_point, array[-1])
				distance = min(distance_to_first, distance_to_last)

				if distance < closest_distance and distance_to_first < distance_to_last:
					closest_array = array
					closest_distance = distance
				elif distance < closest_distance and distance_to_first > distance_to_last:
					closest_array = array[::-1]

					closest_distance = distance

			sorted_arrays.append(closest_array)
			print(sorted_arrays)
			current_point = closest_array[-1]
			try:
				remaining_arrays.remove(closest_array)
			except:
				remaining_arrays.remove(closest_array[::-1])
		return sorted_arrays	
	n = find_longest_shortest_path(components)
#	print(n)
	longest_paths = find_longest_shortest_path(components)
	ordered_arrays = sort_coordinate_arrays(longest_paths, start, end)
#	print(ordered_arrays)

	print(ordered_arrays)
	def flatten_array(array):
		flattened = []
		for sublist in array:
			flattened.extend(sublist)
		return flattened

	result1 = flatten_array(ordered_arrays)
	print(result1)


	#print(longest_paths)
	#print(longest_paths)
	#print(flattened_components)
	x = [p[0] for p in result1]
	y = [p[1] for p in result1]
	plt.plot(x,y)
	plt.gca().invert_yaxis()
	plt.savefig('result.png')


else:
	short_path = shortest_path(start,end,coordinates)
	print(short_path)
	x = [p[0] for p in short_path]
	y = [p[1] for p in short_path]
	plt.plot(x,y)
	plt.gca().invert_yaxis()
	plt.savefig('result.png')
