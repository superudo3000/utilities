#!/usr/bin/ruby

# Find files with an Unicode BOM (Byte Order Mark) for UTF-8 encoding (which
# doesn't actually say anything about byte order as that is a non-issue with
# UTF-8).
#
# See http://en.wikipedia.org/wiki/Byte_Order_Mark
#
# Copyright (c) 2008 Jochen Kupperschmidt <http://homework.nwsnet.de/>
# Version: 14-Jul-2008
# Released under the terms of the MIT License.

require 'find'
require 'optparse'


# Create option parser.
options = {}
ARGV.options do |opts|
  opts.banner << " <path>"
  opts.on("-v", "--[no-]verbose", "run verbosely") do |v|
    options[:verbose] = v
  end
end.parse!

# Check for required path argument.
path = ARGV[0] or (STDERR.puts ARGV.options; exit 2)

# Recursively scan files for the first bytes.
Find.find(path) do |fn|
  next if not File.file?(fn)
  has_bom = File.open(fn) {|f| f.read(3)} == "\xEF\xBB\xBF"
  if options[:verbose]
    # List every scanned file and the corresponding result.
    puts fn << " ... " << (has_bom ? "BOM found." : "no BOM.")
  elsif has_bom
    # Only list names of files with BOMs found.
    puts fn
  end
end
