-- Chạy trong Supabase → SQL Editor → Run
create table if not exists comments (
  id          bigserial primary key,
  slug        text not null,
  author      text not null check (char_length(author) between 1 and 60),
  body        text not null check (char_length(body) between 1 and 3000),
  created_at  timestamptz not null default now(),
  approved    boolean not null default true,
  ip_hash     text
);

create index if not exists comments_slug_idx on comments (slug, created_at desc);

alter table comments enable row level security;

drop policy if exists "public read approved" on comments;
create policy "public read approved"
  on comments for select using (approved = true);

drop policy if exists "public insert" on comments;
create policy "public insert"
  on comments for insert with check (approved = true);

-- chống spam: tối đa 5 bình luận / 10 phút / 1 slug / 1 IP
create or replace function rate_limit_comments() returns trigger
language plpgsql security definer as $$
declare cnt int;
begin
  if new.ip_hash is null then return new; end if;
  select count(*) into cnt from comments
   where slug = new.slug and ip_hash = new.ip_hash
     and created_at > now() - interval '10 minutes';
  if cnt >= 5 then
    raise exception 'Quá nhiều bình luận, vui lòng thử lại sau.';
  end if;
  return new;
end $$;

drop trigger if exists comments_rate_limit on comments;
create trigger comments_rate_limit before insert on comments
for each row execute function rate_limit_comments();
