import unittest

def snp_contig_location(flag, pos, adjusted_bp_location, alignment_length):
	""" determine new bp position of the snp on the larger contig"""
	try:
		""" make sure a number was passed in, if not return empty bp """
		adjusted_bp_location / 1
	except:
		return '-' 
	if flag == 0 or flag == 256:
		""" forward aligment, add adj_bp to pos"""
		return (pos + adjusted_bp_location - 1 )
	elif flag == 16 or flag == 272:
		return (pos + alignment_length - adjusted_bp_location)
	else:
		return '-'

def compliment_name(name, flag):
	""" if the alignment is a reverse, add _comp to the end of its identification """
	if flag == 16 or flag == 272:
		return '%s_comp' % (name)
	else:
		return name
		
def match_snp(allele):
	""" return the complimentary nucleotide for an
		input string of a single nucleotide.
		missing bp (N) will return a N. """
	allele = allele.upper()
	if allele == 'A':
		return 'T'
	elif allele == 'T':
		return 'A'
	elif allele == 'C':
		return 'G'
	elif allele == 'G':
		return 'C'
	elif allele == 'N':
		return 'N'
	else: 
		raise ValueError(
			'Need valid nucleotide (ATGC) or N\n %s was passed in ' % (allele))


def allele_comp_check(in_allele, flag):
	""" if alignment is a reverse, flip the alleles to the complimentary nucleotides """
	if flag == 0 or flag == 256:
		return in_allele
	elif flag == 16 or flag == 272:
		if len(in_allele) == 1:
			return match_snp(in_allele)
		else:
			in_alleles = in_allele.split(',')
			out_alleles = []
			for i in in_alleles:
				out_alleles.append(match_snp(i))
			return ','.join(out_alleles)


class SamTests(unittest.TestCase):
	def test_snp_contig_location(self):	
		self.assertEqual(
					snp_contig_location(0, 100, 12, 50),
					111)
		self.assertEqual(
					snp_contig_location(256, 100, 24, 50),
					123)
		self.assertEqual(
					snp_contig_location(16, 100, 12, 50),
					138)
		self.assertEqual(
					snp_contig_location(272, 100, 24, 50),
					126)
	
	def test_compliment_name(self):
		self.assertEqual(
					compliment_name('CMN001', 0),
					'CMN001')
		self.assertEqual(
					compliment_name('CMN001', 16),
					'CMN001_comp')
		self.assertEqual(
					compliment_name('CMN001', 256),
					'CMN001')	
		self.assertEqual(
					compliment_name('CMN001', 272),
					'CMN001_comp')		
														
	def test_match_snp(self):
		self.assertEqual(
					match_snp('A'),
					'T')
		self.assertEqual(
					match_snp('T'),
					'A')
		self.assertEqual(
					match_snp('C'),
					'G')
		self.assertEqual(
					match_snp('G'),
					'C')
		self.assertRaises(ValueError, match_snp, 'F')

	def test_allele_comp_check(self):
		self.assertEqual(
			allele_comp_check('A,C', 16),
			'T,G')
		self.assertEqual(
			allele_comp_check('A,C', 0),
			'A,C')
		self.assertEqual(
			allele_comp_check('A,C,G', 272),
			'T,G,C')
		self.assertEqual(
			allele_comp_check('A', 16),
			'T')


if __name__ == "__main__":

	unittest.main()

