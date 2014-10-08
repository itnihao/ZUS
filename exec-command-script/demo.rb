#!/usr/bin/env ruby
#by orbs
#version 
#email 
#doc
require 'rubygems'
require 'net/ssh'
require 'colorize'

if ARGV[0] == "hostfile" and ARGV[1] == "commandfile" then
	hostlists=[]
	comdlists=[]
	File.open("commandfile") do |commands|
		while command=commands.gets
			command.split('\n').each do |comd|
				comdlists << comd
			end
		end
	end
	File.open("hostfile") do |lines|
		while line=lines.gets
			line.split(' ').each do |word|
				hostlists << word
			end
			@host=hostlists[0]
			@port=hostlists[1].to_i
			@pass=hostlists[2]
			Net::SSH.start(@host,'root',:password=>@pass,:port=>@port) do |ssh|
				comdlists.map do |com| 
					result=ssh.exec!(com)
					puts "Exec command on #@host succ :)".green
				end
			end
#			hostlists=[]
		end
	end
else
	puts "Usage:\n".red
	puts "ruby foo.rb hostfile commandfile\n".red
	puts "Or ./foo.rb hostfile commandfile ".red
end

