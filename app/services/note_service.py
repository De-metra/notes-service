from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.note import Note
from app.schemas.note import NoteCreate

async def get_all_notes(session: AsyncSession):
    query = await session.execute(select(Note))
    db_notes = query.scalars().all()

    return db_notes

async def get_note_by_id(id: int, session: AsyncSession):
    query = await session.execute(select(Note).where(Note.id == id))
    db_note = query.scalar_one_or_none()

    return db_note

async def create_note(note: NoteCreate, session: AsyncSession):
    db_note = Note(
        title=note.title, 
        content=note.content
    )
    session.add(db_note)
    await session.commit()
    session.refresh(db_note)
    return db_note

async def update_note(id: int, note_data: NoteCreate, session: AsyncSession):
    db_note = await session.get(Note, id)

    if db_note:
        db_note.title = note_data.title
        db_note.content = note_data.content
        await session.commit()
        session.refresh(db_note)
    return db_note

async def update_archive_status(id: int, session: AsyncSession):
    db_note = await session.get(Note, id)

    if db_note: 
        db_note.is_archived = not db_note.is_archived
        await session.commit()
        session.refresh(db_note)
    return db_note

async def delete_note_by_id(id: int, session: AsyncSession):
    db_note = await session.get(Note, id)

    if not db_note: 
        return None
    
    await session.delete(db_note)
    await session.commit()
    return 1
