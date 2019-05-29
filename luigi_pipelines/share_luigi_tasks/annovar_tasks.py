import luigi

from main import *
from toolkit import run_cmd, valid_path


#########14
class Annovar1(luigi.Task):
    sampleID = luigi.Parameter()
    dry_run = luigi.BoolParameter(default=False)

    def requires(self):
        "abstract for implement"
        pass
        # return CombineVariants(sampleID=self.sampleID,
        #                        dry_run=self.dry_run)

    def output(self):
        return luigi.LocalTarget(self.input().path.replace('.merged.vcf', '.merged.av'))

    def run(self):
        valid_path(self.output().path, check_ofile=1)
        cmdline = "%s/convert2annovar.pl %s --includeinfo -format vcf4 > %s" % (
            annovar_pro,
            self.input().path,
            self.output().path)
        run_cmd(cmdline, dry_run=self.dry_run)


class Annovar2(luigi.Task):
    sampleID = luigi.Parameter()
    dry_run = luigi.BoolParameter(default=False)

    def requires(self):
        "abstract for implement"
        pass
        # return Annovar1(sampleID=self.sampleID,
        #                 dry_run=self.dry_run)

    def output(self):
        return luigi.LocalTarget(
            self.input().path.replace('.merged.av',
                                      '.merged.anno.%s_multianno.csv' % genome_version))

    def run(self):
        valid_path(self.output().path, check_ofile=1)
        prefix = self.input().path.rpartition('.merged.av')[0]
        cmdline = "{annovar_dir}/table_annovar.pl {input_f} {annovar_db} -buildver {genome_version} -protocol {db_names} -operation g,r,r,f,f,f,f,f,f -nastring . --remove --otherinfo --csvout --thread {annovar_thread} --outfile {output_f} --argument '-exonicsplicing -splicing 25',,,,,,,,".format(
            annovar_dir=annovar_pro,
            input_f=self.input().path,
            annovar_db=annovar_db,
            genome_version=genome_version,
            db_names=db_names,
            annovar_thread=annovar_thread,
            output_f=prefix + '.merged.anno')
        run_cmd(cmdline, dry_run=self.dry_run)