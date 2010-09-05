#!/usr/bin/ruby

require 'fuck'

if (ARGV.length != 1) then
	puts "go away"
	exit
end

word = ARGV[0]

puts "playing with #{word}"

SDL.init(SDL::INIT_AUDIO | SDL::INIT_JOYSTICK | SDL::INIT_VIDEO)
SDL::Mixer.open

@fuck_sounds = []
@guitar = nil

def poll_events
	while event = SDL::Event.poll
		case event
			when SDL::Event::JoyAxis
			puts "axis: #{event.axis}, #{event.value}"
			if (event.value != 0)  then
				for button in @buttons do
					if (@guitar.button(button)) then
						play_sound(@fuck_sounds[@sound_button_map[button]])
					end
				end
			end
			when SDL::Event::Quit
				break
		end
	end		
end

def run_main
	while true do
		poll_events	

		SDL.delay(33)
	end
end

if (SDL::Joystick.num == 0) then
	puts "no joystick"
	exit
end

@guitar = SDL::Joystick.open(0)
SDL::Joystick.poll = true

#info = get_json_data(word)
#urls = info["items"].map{|item| item["pathogg"]}
#urls.shuffle!
#urls = urls[1..5]
#@fuck_sounds = urls.map{|url| get_ogg(url)}
@fuck_sounds = (1..5).to_a.map{|i| load_ogg("sounds/cunt#{i}.ogg")}

run_main



