create table imdb_kaggle (
	id SERIAL not null primary key,
	title text not null,
	released_year int not null,
	certificate text,
	runtime int not null,
	genre1 text,
	genre2 text,
	genre3 text,
	imdb numeric(2,1) not null,
	overview text not null,
	meta_score smallint,
	director text not null,
	star1 text not null,
	star2 text not null,
	star3 text not null,
	star4 text not null,
	votes int8 not null,
	gross int8
);