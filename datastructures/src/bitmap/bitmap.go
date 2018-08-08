package bitmap

type BitMap struct {
	words []uint64
}

func (m *BitMap) Add(x int) {
	if m == nil {
		m = &BitMap{words: make([]uint64, 0)}
	}
	word, bit := x/64, uint64(x%64)
	for word >= len(m.words) {
		m.words = append(m.words, 0)
	}
	m.words[word] |= 1 << bit
}

func (m *BitMap) Discard(x int) {
	if m == nil {
		return
	}
	word, bit := x/64, uint64(x%64)
	if word >= len(m.words) {
		return
	}
	m.words[word] &= ^(1 << bit)
}

func (m *BitMap) Contain(x int) bool {
	if m == nil {
		return false
	}
	word, bit := x/64, uint64(x%64)
	if word >= len(m.words) {
		return false
	}
	return word < len(m.words) && m.words[word]&(1<<bit) != 0
}

func (m *BitMap) Union(s BitMap) {
	for i, sword := range s.words {
		if i < len(m.words) {
			m.words[i] |= sword
		} else {
			m.words = append(m.words, sword)
		}
	}
}

func (m *BitMap) Intersection(s BitMap) {
	for i, sword := range s.words {
		if i < len(m.words) {
			m.words[i] &= sword
		}
	}
	m.gc()
}

func (m *BitMap) Difference(s BitMap) {
	for i, sword := range s.words {
		if i < len(m.words) {
			m.words[i] &= ^sword
		}
	}
	m.gc()
}

func (m *BitMap) IsEmpty() bool {
	return m.words == nil || m.gc()
}

func (m *BitMap) Clone() BitMap {
	var m2 BitMap
	if len(m.words) == 0 {
		return m2
	}
	m2.words = make([]uint64, len(m.words))
	copy(m2.words, m.words)
	return m2
}

func (m *BitMap) Clear() { m.words = nil }

func (m *BitMap) gc() bool {
	var CannotGC bool
	for _, mword := range m.words {
		if mword != 0 {
			CannotGC = true
		}
	}
	if !CannotGC {
		m.words = nil
	}
	return !CannotGC
}
