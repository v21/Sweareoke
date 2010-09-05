#!/usr/bin/ruby

require 'net/http'
require 'json'
require 'sdl'

class Array
  def shuffle!
    size.downto(1) { |n| push delete_at(rand(n)) }
    self
  end
end

def get_json_data(word)
	api_key = "eab344983932fb9d55ddfdb20e36e8cf"

	api_url_start = "http://apifree.forvo.com/action/word-pronunciations/format/json/word/"
	api_url_end = "/language/en/key/"

	#word = "fuck"

	url = URI.parse(api_url_start+word+api_url_end+api_key)
	request = Net::HTTP::Get.new(url.path)
	response = Net::HTTP.start(url.host, url.port) {|http| http.request(request) }
	info = JSON.parse(response.body)

	return info
end

def get_ogg(url)
	system("wget #{url}")
	filename = url.split("/").last
	system("mv #{filename} sounds/#{filename}")
	return load_ogg("sounds/#{filename}")
end

def load_ogg(filename)
	return SDL::Mixer::Wave.load(filename)
end

def play_sound(sound)
	SDL::Mixer.play_channel(-1, sound, 0)
end

@red = 1
@green = 5
@yellow = 0
@blue = 2
@orange = 3
@tip = 4
@start = 9
@select = 8

@sound_button_map = {
	@green => 0,
	@red => 1,
	@yellow => 2,
	@blue => 3,
	@orange => 4
}

@buttons = [@green, @red, @yellow, @blue, @orange]
