"""
Inserts / updates README.md based on README_template.md.
Also prints out some colored statistics in the terminal.

Use without parameters.

Assumes AoC formatted ranks within the input/personal-times-ranks-scores folder.

Currently, GitHub is not on mermaid version required for xycharts (10.6.1). Hence,
the template contains a reference to the `cumulative-rank-frequency.svg` which needs to
be kept up to date. Use an online tool to convert the xychart mermaid to svg and remove
the mermaid part from the README.md before committing.
(`https://mermaid.live/` does not offer svg export so take it directly from the DOM
and format it with `https://jsonformatter.org/xml-formatter`)
"""

import itertools as it
import math
import os
import re

def colored(text, color='w'):
	color_code = ''
	match color:
		case 'r': color_code = '91m'
		case 'g': color_code = '92m'
	if color_code == '':
		return text
	return '\033[' + color_code + text + '\033[0m'

def get_color_within_gradient(gradient_by_color_pairs: list[tuple[str, str]],
		relative_position: float) -> str:
	if relative_position >= 1:
		return gradient_by_color_pairs[-1][1]
	if relative_position < 0:
		return gradient_by_color_pairs[0][0]
	grad_by_int_pairs = [
		tuple(
			tuple(int(coge, 16) for coge in [cog[:2], cog[2:4], cog[4:]])
			for cog in gbycp
		)
		for gbycp in gradient_by_color_pairs
	]
	grad_interval_idx = math.floor(len(grad_by_int_pairs) * relative_position)
	weight_on_upper_bound = relative_position * len(grad_by_int_pairs) - grad_interval_idx
	int_color = 0
	for lo, hi in zip(*grad_by_int_pairs[grad_interval_idx]):
		int_color *= 256
		int_color += math.floor((1 - weight_on_upper_bound) * lo + weight_on_upper_bound * hi)
	res = f'{int_color:06x}'
	return res

def color_for_value(value, minimum, maximum, small_is_good):
	if not small_is_good:
		maximum, minimum = minimum, maximum
	if value == minimum:
		return 'g'
	if value == maximum:
		return 'r'
	return 'w'

def get_formatted_history_line(line, col_widths, colors=None):
	if colors is None:
		colors = ['w'] * len(col_widths)
	return ' | '. join([
		colored((' ' * cw + e)[-cw:], cl) for cw, e, cl in zip(col_widths, line, colors)
	])

def get_formatted_history_tab(table, small_is_good=True, in_color=True):
	val_tab = [[int(e.replace('%', '')) for e in l] for l in table[1:]]
	col_widths = [max(len(e) for e in col) for col in zip(*table)]
	col_extremes = [(min(col), max(col)) for col in zip(*val_tab)]
	result = []
	result.append(get_formatted_history_line(table[0], col_widths))
	result.append('=' * (sum(col_widths) + (len(col_widths) - 1) * 3))
	for l, val_row in zip(table[1:], val_tab):
		if not in_color:
			result.append(get_formatted_history_line(l, col_widths))
		else:
			colors = [
				color_for_value(v, mi, ma, small_is_good)
				for (mi, ma), v in zip(col_extremes, val_row)
			]
			colors[0] = 'w'
			result.append(get_formatted_history_line(l, col_widths, colors))
	return result

class Participation:
	def __init__(self, year, line, star_num: int):
		self.year = year
		ints = [int(e) for e in re.findall(r'(\d+)', line)]
		self.day = ints[0]
		base_idx = 1 if star_num == 1 else 6
		self.time = ((ints[base_idx] * 60) + ints[base_idx + 1]) * 60 + ints[base_idx + 2]
		self.rank = ints[base_idx + 3]
		self.score = ints[base_idx + 4]

def get_participations():
	result = []
	dir_path = 'input/personal-times-ranks-scores/'
	for input_file in os.listdir(dir_path):
		year = input_file.split('/')[-1].replace('.txt', '')
		with open(dir_path + input_file, 'r') as f:
			lines = f.read().strip().split('\n')
		for l in lines[2:]:
			for star_num in range(1, 3):
				result += [Participation(year, l, star_num)]
	return result

def get_years(participations):
	return list(sorted(set(p.year for p in participations)))

def get_participations_by_year(participations, year):
	return [p for p in participations if p.year == year]

def get_rank_quantile(participations, quantile_in_percent):
	sp = sorted(participations, key=lambda p: p.rank)
	idx = max(0, math.ceil(len(participations) * quantile_in_percent / 100) - 1)
	return sp[idx].rank

def get_rank_frequency(participations, rank, digits=0) -> float | int:
	f_in_perc = sum(p.rank <= rank for p in participations) * 100
	if digits:
		return f_in_perc * 10**digits // len(participations) / 10**digits
	return f_in_perc // len(participations)

def get_rank_buckets():
	return [100, 150, 200, 300, 500, 700, 1000, 1500, 2000, 3000, 5000]

def get_color_series():
	return ['f84', '1d6', '77f', 'ee5', 'd6d', '3dd']

def get_history(participations):
	years = get_years(participations)
	rank_buckets = get_rank_buckets()
	rank_labels = [str(r) for r in rank_buckets]
	quantile_buckets = [0, 5, 10, 20, 30, 50, 75, 90, 100]
	quantile_labels = [f'{q}%' for q in quantile_buckets]
	quantile_labels[0] = 'Best'
	quantile_labels[next(i for i, v in enumerate(quantile_buckets) if v == 50)] = 'Median'
	quantile_labels[-1] = 'Worst'
	quantile_tab = [['Year'] + quantile_labels]
	for y in years:
		py = get_participations_by_year(participations, y)
		quantile_tab += [[y] + [f'{get_rank_quantile(py, q)}' for q in quantile_buckets]]
	rank_tab = [['Year'] + rank_labels]
	for y in years:
		py = get_participations_by_year(participations, y)
		rank_tab += [[y] + [f'{get_rank_frequency(py, r)}%' for r in rank_buckets]]
	return quantile_tab, rank_tab

def print_history():
	participations = get_participations()
	quantile_tab, rank_tab = get_history(participations)
	print('\n###################\n# RANKS\n###################\n')

	print('\n'.join(get_formatted_history_tab(quantile_tab)))
	print()
	print('\n'.join(get_formatted_history_tab(rank_tab, small_is_good=False)))

def dashboard_overview(participations):
	rank_buckets = [0] + get_rank_buckets() + [max(p.rank for p in participations)]
	occurrence_by_rank = [
		(sum(r_before < p.rank <= r for p in participations), r_before, r)
		for r_before, r in it.pairwise(rank_buckets)
	]
	# mermaid always sorts pie charts -> use colors to make gradual semantics clear
	# sort colors descending for occurrence / ascending for ranks (as mermaid does)
	# also adjust series order because old mermaid versions do _not_ sort the legend
	res = '```mermaid'
	col_gradient = [
		# extra long green [1, 500] due to multiple tiny intervals
		('80ff80', '40a040'), ('40a040', '004000'),
		('00a0ff', '003060'), # blue/cyan for [501, 1000]
		('ffff00', '606000'), # yellow [1001, 2000]
		('ff4040', '600000'), # red the rest
	]
	pie_num = len(occurrence_by_rank)
	pie_colors_and_occ = [
		((o, -r), get_color_within_gradient(col_gradient, i / (pie_num - 1)), (o, rb, r))
		for i, (o, rb, r) in enumerate(occurrence_by_rank)
	]
	pie_colors_and_occ.sort(reverse=True)
	pie_colors_str = ', '.join(
		f'"pie{i+1}": "#{pc}"'
		for i, (_, pc, _) in enumerate(pie_colors_and_occ)
	)
	res += '\n%%{init: {"themeVariables": {' + pie_colors_str + '}}}%%'
	res += '\npie'
	res += '\ntitle Ranking within Top-k Segment'
	for *_, (o, r_before, r) in pie_colors_and_occ:
		res += f'\n"{o} * [{r_before + 1}, {r}]": {o}'
	res += '\n```'
	return res

def dashboard_history_tables(participations):
	quantile_tab, rank_tab = [
		'\n'.join(get_formatted_history_tab(h, in_color=False))
		for h in get_history(participations)
	]
	res = f'Rank by Quantile\n```\n{quantile_tab}\n```'
	res += f'\nFrequency by Rank\n```\n{rank_tab}\n```'
	return res

def dashboard_history_charts(participations):
	years = get_years(participations)
	color_series = get_color_series()
	rank_buckets = get_rank_buckets()
	chart_quantiles = [0, 25, 50, 75, 100]
	res = '\n```mermaid'
	res += '\nflowchart TD '
	for y, c in zip(years, color_series):
		res += f'\nstyle {y} fill:#{c},stroke:#333,stroke-width:2px,color:#fff'
	res += '\n```'
	res += '\n\n```mermaid'
	res += '\n---'
	res += '\nconfig:'
	res += '\n themeVariables:'
	res += '\n  xyChart:'
	plot_color_palette = ['#808080'] * len(chart_quantiles) \
		+ [f'#{c}' for _, c in zip(years, color_series)]
	res += f'\n   plotColorPalette: "{', '.join(plot_color_palette)}"'
	res += '\n---'
	res += '\nxychart-beta'
	res += '\ntitle "Frequency of Ranking within Top-k"'
	res += '\nx-axis ' + str(rank_buckets)
	res += '\ny-axis "Frequency (in %)" 0 --> 100'
	for q in chart_quantiles:
		res +=f'\nline "{q}%" {str([q] * len(rank_buckets))}'
	for y in years:
		res += f'\nline "{y}" ' + str([
			get_rank_frequency(get_participations_by_year(participations, y), r)
			for r in rank_buckets
		])
	res += '\n```'
	return res

def export_dashboard():
	with open('README_template.md', 'r') as f:
		result = f.read()
		f.close()
	participations = get_participations()
	result = result.replace('{overall}', dashboard_overview(participations))
	result = result.replace('{history_charts}', dashboard_history_charts(participations))
	result = result.replace('{history_tables}', dashboard_history_tables(participations))
	with open('README.md', 'w') as f:
		f.write(result)
		f.close()
	print('\nREADME.md inserted / updated!')

print_history()
export_dashboard()
