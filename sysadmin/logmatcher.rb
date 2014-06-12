#!/usr/bin/ruby

# Skim through Apache access log files and count the number of hits to URLs
# matching a given pattern.
#
# Copyright (c) 2008 Jochen Kupperschmidt <http://homework.nwsnet.de/>
# Version: 07-Aug-2008
# Released under the terms of the MIT License.

require 'zlib'


# Adjust this.
regex = /GET (\/media\/videos\/\d{4}-\d{2}-\d{2})/
# TODO: Might be nice to be able to pass this expression as command line
#       argument.


class HitCounter

  def initialize(regex)
    @regex = regex
    # Create a hash with a default value of zero.
    @hits = Hash.new { |hash, key| hash[key] = 0 }
  end

  def parse_file(fname)
    # Read a file, line by line.  If the file name ends on '.gz', treat it as
    # gzip-compressed and decompress it.  Count the occurences of each matched
    # URL separately.
    puts "Parsing #{fname} ..."
    f = (fname =~ /\.gz$/ ? Zlib::GzipReader : File).open(fname)
    f.each_line { |line| @hits[$+] += 1 if line =~ @regex }
  end

  def show_results
    # Display the results of matching URLs and how often they were accessed.
    puts "\nResults:"
    @hits.each { |details| puts "%s %8d hits" % details }
  end

  def self.batch(regex, fnames)
    # A shortcut class method to parse multiple files and display the result.
    fnames = Dir['access.log*'] if ARGV.empty?
    (STDERR.puts "No files given."; exit 2) if fnames.empty?
    puts "Going to analyze #{fnames.length} files ..."
    instance = self.new(regex)
    begin
      fnames.each { |fname| instance.parse_file(fname) }
      instance.show_results
    rescue Interrupt
      puts "\nAborted."
    end
  end

end


HitCounter::batch(regex, ARGV)
