package log

import (
	mdlog "github.com/asim/go-micro/v3/debug/log"
)

type logStream struct {
	stream <-chan mdlog.Record
	stop   chan bool
}

func (l *logStream) Chan() <-chan mdlog.Record {
	return l.stream
}

func (l *logStream) Stop() error {
	select {
	case <-l.stop:
		return nil
	default:
		close(l.stop)
	}
	return nil
}
