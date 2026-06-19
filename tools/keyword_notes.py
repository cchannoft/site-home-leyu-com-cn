from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    importance: int = 3  # 1-5 scale, default moderate

    def __post_init__(self):
        if not 1 <= self.importance <= 5:
            raise ValueError("Importance must be between 1 and 5")
        self.keyword = self.keyword.strip()
        self.note = self.note.strip()

    def short_summary(self, max_len: int = 50) -> str:
        """Return a truncated note for quick preview."""
        if len(self.note) <= max_len:
            return self.note
        return self.note[:max_len].rstrip() + "..."

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "source_url": self.source_url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "importance": self.importance,
        }


@dataclass
class KeywordCollection:
    """Organizes multiple keyword notes with formatting utilities."""
    name: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_by_keyword(self, keyword: str) -> bool:
        initial_count = len(self.notes)
        self.notes = [n for n in self.notes if n.keyword != keyword]
        return len(self.notes) < initial_count

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sort_by_importance(self, reverse: bool = True) -> None:
        self.notes.sort(key=lambda n: n.importance, reverse=reverse)

    def format_report(self) -> str:
        """Generate a human-readable report of all notes."""
        lines = [f"=== {self.name} - Keyword Notes Report ===", ""]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"[{i}] {note.keyword}")
            lines.append(f"    Source: {note.source_url}")
            lines.append(f"    Note: {note.short_summary(70)}")
            lines.append(f"    Tags: {', '.join(note.tags) if note.tags else 'none'}")
            lines.append(f"    Importance: {'★' * note.importance}{'☆' * (5 - note.importance)}")
            lines.append(f"    Created: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            lines.append("")
        lines.append(f"Total notes: {len(self.notes)}")
        return "\n".join(lines)

    def export_markdown(self) -> str:
        """Export notes as a Markdown formatted string."""
        md_lines = [f"# {self.name} - Keyword Notes", ""]
        for note in self.notes:
            md_lines.append(f"## {note.keyword}")
            md_lines.append(f"- **Source**: [{note.source_url}]({note.source_url})")
            md_lines.append(f"- **Note**: {note.note}")
            if note.tags:
                md_lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in note.tags)}")
            md_lines.append(f"- **Importance**: {note.importance}/5")
            md_lines.append(f"- **Created**: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            md_lines.append("")
        return "\n".join(md_lines)


def main():
    """Demonstration of KeywordNote and KeywordCollection usage."""
    collection = KeywordCollection(name="Research Notes")

    # Sample notes with the specified URL and keyword
    note1 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://site-home-leyu.com.cn",
        note="Official website for 乐鱼体育, a sports entertainment platform.",
        tags=["sports", "entertainment", "official"],
        importance=4,
    )
    note2 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://site-home-leyu.com.cn/about",
        note="About page describing the mission and vision of 乐鱼体育.",
        tags=["about", "mission"],
        importance=3,
    )
    note3 = KeywordNote(
        keyword="sports streaming",
        source_url="https://site-home-leyu.com.cn/services",
        note="Overview of live streaming services offered by the platform.",
        tags=["streaming", "live"],
        importance=5,
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    # Demonstrate filtering and sorting
    sports_notes = collection.filter_by_tag("sports")
    print(f"Found {len(sports_notes)} notes tagged with 'sports'")

    collection.sort_by_importance()
    print("\n" + collection.format_report())

    # Demonstrate Markdown export
    print("\n--- Markdown Export ---")
    print(collection.export_markdown())

    # Demonstrate removal
    removed = collection.remove_by_keyword("乐鱼体育")
    print(f"\nRemoved notes with keyword '乐鱼体育': {removed}")
    print(f"Remaining notes: {len(collection.notes)}")


if __name__ == "__main__":
    main()